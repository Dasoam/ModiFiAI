import streamlit as st
from datetime import datetime
import time
import requests
from pipeline import start_pipeline

API_BASE_URL = "http://localhost:8000"


def save_comment_via_api(data):
    try:
        response = requests.post(f"{API_BASE_URL}/comments/", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error saving comment: {e}")
        return None


def get_comments_via_api():
    try:
        response = requests.get(f"{API_BASE_URL}/comments/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching comments: {e}")
        return []


def get_pending_comments_via_api():
    try:
        response = requests.get(f"{API_BASE_URL}/comments/pending")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching pending comments: {e}")
        return []


def update_comment_status_via_api(comment_id, new_status):
    try:
        status_bool = True if new_status == "true" else False
        response = requests.put(f"{API_BASE_URL}/comments/{comment_id}", json=status_bool)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating comment: {e}")
        return None


def main():
    st.set_page_config(page_title="Comment Moderation System", layout="wide")

    if "processed_result" not in st.session_state:
        st.session_state.processed_result = None

    # API Status Check
    try:
        response = requests.get(f"{API_BASE_URL}/")
        api_status = "🟢 Connected"
    except:
        api_status = "🔴 API Offline"

    st.sidebar.write(f"**API Status:** {api_status}")

    tab1, tab2, tab3 = st.tabs(["Check Comment", "All Comments", "Pending Moderation"])

    with tab1:
        st.header("📝 Comment Analysis Pipeline")
        comment = st.text_area("Enter comment to analyze:", height=150, placeholder="Type your comment here...")

        if st.button("🔍 Analyze Comment", type="primary"):
            if comment.strip():
                with st.spinner("Analyzing comment..."):
                    try:
                        processed_result = start_pipeline(comment)
                        processed_result["timestamp"] = datetime.now().isoformat()
                        processed_result["username"] = "user"

                        api_result = save_comment_via_api(processed_result)
                        if api_result:
                            st.session_state.processed_result = processed_result
                            st.success("✅ Analysis complete!")
                        else:
                            st.error("❌ Failed to save comment")
                    except Exception as e:
                        st.error(f"❌ Error processing comment: {str(e)}")
            else:
                st.warning("Please enter a comment to analyze.")

        if st.session_state.processed_result:
            st.subheader("📊 Analysis Result")
            result = st.session_state.processed_result

            status_colors = {
                "true": ("🟢", "success"),
                "false": ("🔴", "error"),
                "check": ("🟡", "warning")
            }

            icon, color = status_colors.get(result["published"], ("⚪", "info"))

            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Status", f"{icon} {result['published'].upper()}")
            with col2:
                st.write(f"**Reason:** {result['reason']}")

            st.write("**Original Comment:**")
            st.code(result["comment"])

    with tab2:
        st.header("📋 All Saved Comments")

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Refresh"):
                st.rerun()

        all_comments = get_comments_via_api()

        if not all_comments:
            st.info("No comments found in the database.")
        else:
            st.write(f"**Total Comments:** {len(all_comments)}")

            for i, comment in enumerate(all_comments, 1):
                with st.expander(
                        f"Comment #{i} - {comment.get('username', 'user')} ({comment.get('published', 'unknown').upper()})"):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**Comment:** {comment.get('comment', 'N/A')}")
                        st.write(f"**Reason:** {comment.get('reason', 'N/A')}")
                        st.write(f"**Timestamp:** {comment.get('timestamp', 'N/A')}")
                        st.write(f"**ID:** {comment.get('_id', 'NO ID')}")  # SAFE ACCESS

                    with col2:
                        status_colors = {
                            "true": "🟢 Published",
                            "false": "🔴 Rejected",
                            "check": "🟡 Pending"
                        }
                        st.write(f"**Status:**")
                        st.write(status_colors.get(comment.get('published'), "⚪ Unknown"))

    with tab3:
        st.header("⚖️ Pending Moderation")

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Refresh", key="refresh_pending"):
                st.rerun()

        pending_comments = get_pending_comments_via_api()

        if not pending_comments:
            st.info("🎉 No comments pending moderation!")
        else:
            st.write(f"**Comments Awaiting Review:** {len(pending_comments)}")
            st.divider()

            for i, comment in enumerate(pending_comments, 1):
                if '_id' not in comment:
                    st.error(f"Comment {i} missing ID: {comment}")
                    continue

                st.subheader(f"Comment #{i}")

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**👤 User:** {comment.get('username', 'user')}")
                    st.write(f"**💬 Comment:**")
                    st.code(comment.get('comment', 'N/A'))
                    st.write(f"**🔍 AI Analysis:** {comment.get('reason', 'N/A')}")
                    st.write(f"**📅 Submitted:** {comment.get('timestamp', 'N/A')}")
                    st.write(f"**🆔 ID:** {comment['_id']}")

                with col2:
                    st.write("**Actions:**")

                    if st.button("✅ Approve", key=f"approve_{comment['_id']}", type="primary"):
                        result = update_comment_status_via_api(comment["_id"], "true")
                        if result:
                            st.success("Comment approved!")
                            time.sleep(1)
                            st.rerun()

                    if st.button("❌ Reject", key=f"reject_{comment['_id']}", type="secondary"):
                        result = update_comment_status_via_api(comment["_id"], "false")
                        if result:
                            st.success("Comment rejected!")
                            time.sleep(1)
                            st.rerun()

                st.divider()


if __name__ == "__main__":
    main()
