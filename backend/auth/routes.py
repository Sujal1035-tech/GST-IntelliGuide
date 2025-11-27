from fastapi import APIRouter, HTTPException, Response
from backend.db.mongo import users_collection
from backend.auth.utils import hash_password, verify_password
from backend.auth.jwt_handler import create_access_token

router = APIRouter()


# REGISTER USER

@router.post("/register")
def register_user(email: str, username: str, password: str):

    # Check if user already exists
    existing = users_collection.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password
    hashed_pw = hash_password(password)

    # Insert user
    users_collection.insert_one({
        "email": email,
        "username": username,
        "password_hash": hashed_pw,
    })

    return {"message": "User registered successfully"}



# LOGIN USER

@router.post("/login")
def login_user(response: Response, email: str, password: str):

    # Find the user
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create JWT token
    token = create_access_token({"user_id": str(user["_id"])})

    # Save token in HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=24 * 60 * 60,
    )

    return {"message": "Login successful"}

@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
