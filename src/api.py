from fastapi import FastAPI, HTTPException, Body
from bson import ObjectId
from typing import List
from datetime import datetime
from model import CommentIn, CommentOut
from db_connection import save_comment, get_comments, update_published_status

app = FastAPI()


@app.post("/comments/")  # REMOVED response_model
def create_comment(comment: CommentIn):
    try:
        data = comment.dict()
        inserted_id = save_comment(data)
        if not inserted_id:
            raise HTTPException(status_code=500, detail="Failed to insert comment")
        data["_id"] = str(inserted_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating comment: {str(e)}")


@app.get("/comments/")  # REMOVED response_model - THIS IS THE KEY FIX
def read_comments():
    try:
        comments = get_comments()
        result = []

        for c in comments:
            # Convert ObjectId to string
            c["_id"] = str(c["_id"])

            # Handle datetime conversion
            if "timestamp" in c and isinstance(c["timestamp"], datetime):
                c["timestamp"] = c["timestamp"].isoformat()

            # Ensure username exists
            c["username"] = c.get("username", "user")

            result.append(c)

        print(f"API returning: {result}")  # Debug print
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching comments: {str(e)}")


@app.get("/comments/pending")  # REMOVED response_model
def get_pending_comments():
    try:
        comments = get_comments({"published": "check"})
        result = []

        for c in comments:
            c["_id"] = str(c["_id"])

            if "timestamp" in c and isinstance(c["timestamp"], datetime):
                c["timestamp"] = c["timestamp"].isoformat()

            c["username"] = c.get("username", "user")
            result.append(c)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pending comments: {str(e)}")


@app.put("/comments/{comment_id}")
def update_comment_status(comment_id: str, new_status: bool = Body(...)):
    try:
        if not ObjectId.is_valid(comment_id):
            raise HTTPException(status_code=400, detail="Invalid comment ID format")

        status_str = "true" if new_status else "false"
        updated_count = update_published_status(comment_id, status_str)

        if updated_count == 0:
            raise HTTPException(status_code=404, detail="Comment not found or not in 'check' state")

        return {"updated_count": updated_count, "message": f"Comment status updated to {status_str}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating comment: {str(e)}")


@app.get("/")
def root():
    return {"message": "Comment Moderation API", "status": "running"}
