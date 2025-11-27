from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.auth.routes import router as auth_router
from backend.auth.me import router as me_router
from backend.chats.routes import router as chats_router
from backend.chats.websocket import websocket_chat_endpoint

app = FastAPI()

app.include_router(auth_router)
app.include_router(me_router)
app.include_router(chats_router)

@app.websocket("/ws/chat/{chat_id}")
async def chat_websocket(websocket: WebSocket, chat_id: str):
    await websocket_chat_endpoint(websocket, chat_id)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def root():
    return FileResponse("frontend/login.html")