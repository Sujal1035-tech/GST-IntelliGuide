from fastapi import Request, HTTPException, status, WebSocket
from backend.auth.jwt_handler import decode_jwt
from backend.db.mongo import users_collection
from bson import ObjectId


def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = users_collection.find_one({"_id": ObjectId(payload["user_id"])})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# ✔ NEW — WS-compatible version
async def get_current_user_ws(websocket: WebSocket):
    token = websocket.cookies.get("access_token")
    if not token:
        await websocket.close(code=4401)
        raise HTTPException(status_code=401, detail="Not authenticated (WS)")

    payload = decode_jwt(token)
    if not payload:
        await websocket.close(code=4401)
        raise HTTPException(status_code=401, detail="Invalid token (WS)")

    user = users_collection.find_one({"_id": ObjectId(payload["user_id"])})

    if not user:
        await websocket.close(code=4401)
        raise HTTPException(status_code=401, detail="User not found (WS)")

    return user
