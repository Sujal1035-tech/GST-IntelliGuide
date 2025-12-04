from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from backend.db.mongo import users_collection
from backend.auth.utils import hash_password, verify_password
from backend.auth.jwt_handler import create_access_token

router = APIRouter()

# -----------------------------------------------------------
# 1️⃣ Request Model for Registration (REQUIRED!)
# -----------------------------------------------------------
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


# -----------------------------------------------------------
# 2️⃣ REGISTER USER
# -----------------------------------------------------------
@router.post("/register")
def register_user(payload: RegisterRequest):

    existing = users_collection.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(payload.password)

    users_collection.insert_one({
        "email": payload.email,
        "username": payload.name,
        "password_hash": hashed_pw,
    })

    return {"message": "User registered successfully"}


# -----------------------------------------------------------
# 3️⃣ LOGIN USER
# -----------------------------------------------------------
@router.post("/login")
def login_user(response: Response, email: str, password: str):

    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"user_id": str(user["_id"])})

    # set secure cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=24 * 60 * 60,
    )

    return {"message": "Login successful"}


# -----------------------------------------------------------
# 4️⃣ LOGOUT USER
# -----------------------------------------------------------
@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
