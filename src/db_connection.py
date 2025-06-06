from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from logger import logger
from bson import ObjectId

load_dotenv()
user = os.getenv("db_user")
password = os.getenv("password")
db = os.getenv("db_name")

uri = f"mongodb+srv://{user}:{password}@cluster0.decjvw7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

def save_comment(data):
    """
    Save a comment document to the MongoDB collection.
    :param data: dict with keys 'comment', 'published', 'reason'
    """
    try:
        database = client[db]
        collection = database["comments"]  # You can change 'comments' to your desired collection name
        result = collection.insert_one(data)
        logger.info(f"Document inserted with id: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        logger.error(f"Error inserting document: {e}")
        print(e)


# comment_data = {
#     'comment': "This is a test comment.",
#     'published': True,
#     'reason': "Testing save functionality"
# }
# save_comment(comment_data)

def get_comments(filter_query=None):
    """
    Retrieve comments from the MongoDB collection.
    :param filter_query: dict to filter documents (optional)
    :return: list of comment documents
    """
    try:
        database = client[db]
        collection = database["comments"]  # Use your collection name
        if filter_query is None:
            filter_query = {}
        comments = list(collection.find(filter_query))
        logger.info(f"Fetched {len(comments)} comments from the database.")
        return comments
    except Exception as e:
        logger.error(f"Error fetching comments: {e}")
        print(e)
        return []

def update_published_status(comment_id, new_status):
    """
    Update the 'published' status of a comment by its _id.
    :param comment_id: ObjectId of the comment document
    :param new_status: 'true' or 'false' as string
    """
    try:
        database = client[db]
        collection = database["comments"]
        result = collection.update_one(
            {"_id": ObjectId(comment_id), "published": "check"},
            {"$set": {"published": new_status}}
        )
        if result.modified_count:
            logger.info(f"Updated comment {comment_id} published status to '{new_status}'")
        else:
            logger.warning(f"No document updated for comment {comment_id}. It may not be in 'check' state.")
        return result.modified_count
    except Exception as e:
        logger.error(f"Error updating comment: {e}")
        print(e)
        return 0
