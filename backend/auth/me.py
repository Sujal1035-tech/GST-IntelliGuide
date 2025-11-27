from fastapi import APIRouter, Depends
from backend.auth.deps import get_current_user

router = APIRouter()

@router.get("/auth/me")
def auth_me(user = Depends(get_current_user)):
    return {"user": str(user["_id"]), "email": user["email"]}
