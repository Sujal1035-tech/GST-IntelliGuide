from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime

from backend.auth.deps import get_current_user
from backend.db.mongo import chats_collection, messages_collection

router = APIRouter(prefix="/chats", tags=["Chats"])

@router.post("/")
def create_chat(
    title: str | None = None,
    current_user=Depends(get_current_user)
):

    if title is None:
        title = "New Chat"

    chat_data = {
        "user_id": str(current_user["_id"]),
        "title": title,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = chats_collection.insert_one(chat_data)
    chat_data["_id"] = str(result.inserted_id)

    return chat_data

@router.get("/")
def list_chats(current_user=Depends(get_current_user)):
    user_id = str(current_user["_id"])

    chats = list(chats_collection.find({"user_id": user_id}))
    for chat in chats:
        chat["_id"] = str(chat["_id"])
    return chats


@router.get("/{chat_id}/messages")
def get_chat_messages(chat_id: str, current_user=Depends(get_current_user)):
    chat = chats_collection.find_one({"_id": ObjectId(chat_id)})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    if chat["user_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Access denied")

    messages = list(messages_collection.find({"chat_id": chat_id}))

    for msg in messages:
        msg["_id"] = str(msg["_id"])

    return messages
