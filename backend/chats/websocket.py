# backend/chats/websocket.py
import traceback
from datetime import datetime
from bson import ObjectId
from fastapi import WebSocket, WebSocketDisconnect

from backend.auth.deps import get_current_user_ws
from backend.db.mongo import chats_collection, messages_collection
from backend.rag.rag_chain import get_rag_chain


class WebSocketConnectionManager:
    """Manage active WebSocket connections"""

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, chat_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[chat_id] = websocket

    def disconnect(self, chat_id: str):
        if chat_id in self.active_connections:
            del self.active_connections[chat_id]

    async def send_message(self, chat_id: str, message: str):
        ws = self.active_connections.get(chat_id)
        if ws:
            await ws.send_text(message)


manager = WebSocketConnectionManager()
rag_chain = get_rag_chain()


async def websocket_chat_endpoint(websocket: WebSocket, chat_id: str):
    """Full WebSocket GST Chat"""

    current_user = await get_current_user_ws(websocket)

    # 2. Validate chat ID
    try:
        chat_obj_id = ObjectId(chat_id)
    except:
        await websocket.close(code=4001)
        return

    chat = chats_collection.find_one({"_id": chat_obj_id})
    if not chat:
        await websocket.close(code=4004)
        return

    if chat["user_id"] != str(current_user["_id"]):
        await websocket.close(code=4403)
        return

    # 3. Accept connection
    await manager.connect(chat_id, websocket)

    try:
        while True:
            user_text = await websocket.receive_text()

            messages_collection.insert_one({
                "chat_id": chat_id,
                "user_id": str(current_user["_id"]),
                "sender": "user",
                "content": user_text,
                "timestamp": datetime.utcnow(),
            })

            try:
                answer = rag_chain.invoke({"question": user_text}) 

            except Exception as e:
                print("--- RAG CHAIN INVOCATION ERROR ---")
                traceback.print_exc()
                print("-------------------------------------")
                   
                answer = f"Error generating answer. Check console for: {e.__class__.__name__}" 

            if not answer:
                answer = "I could not find relevant GST information."

            # 6. Save bot message
            messages_collection.insert_one({
                "chat_id": chat_id,
                "user_id": str(current_user["_id"]),
                "sender": "bot",
                "content": answer,
                "timestamp": datetime.utcnow(),
            })

            await manager.send_message(chat_id, answer)

    except WebSocketDisconnect:
        manager.disconnect(chat_id)