import os
from datetime import datetime
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "studybot"
COLLECTION_NAME = "chat_history"

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def save_message(session_id: str, user_message: str, bot_response: str):
    """
    Save a user-bot exchange to MongoDB.
    Each session's messages are stored in a single document.
    """
    timestamp = datetime.utcnow()

    # Check if session already exists
    existing = collection.find_one({"session_id": session_id})

    if existing:
        # Append new messages to existing session
        collection.update_one(
            {"session_id": session_id},
            {
                "$push": {
                    "messages": {
                        "$each": [
                            {"role": "user", "content": user_message, "timestamp": timestamp},
                            {"role": "assistant", "content": bot_response, "timestamp": timestamp}
                        ]
                    }
                },
                "$set": {"last_updated": timestamp}
            }
        )
    else:
        # Create a new session document
        collection.insert_one({
            "session_id": session_id,
            "created_at": timestamp,
            "last_updated": timestamp,
            "messages": [
                {"role": "user", "content": user_message, "timestamp": timestamp},
                {"role": "assistant", "content": bot_response, "timestamp": timestamp}
            ]
        })


def get_history(session_id: str) -> list:
    """
    Retrieve all messages for a given session from MongoDB.
    Returns a list of message dicts with role and content.
    """
    session = collection.find_one({"session_id": session_id})

    if not session:
        return []

    # Return messages without MongoDB's internal timestamp for cleaner output
    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in session.get("messages", [])
    ]


def clear_session(session_id: str):
    """Delete all messages for a session."""
    collection.delete_one({"session_id": session_id})
