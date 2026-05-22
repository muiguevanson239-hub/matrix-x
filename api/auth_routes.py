from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from memory.db import Database
from auth.auth import AuthSystem

router = APIRouter(
    tags=["Authentication"]
)

db = Database()
auth = AuthSystem()


# =========================================================
# REQUEST MODELS
# =========================================================

class RegisterRequest(BaseModel):
    user_id: str
    password: str


class LoginRequest(BaseModel):
    user_id: str
    password: str


# =========================================================
# REGISTER
# =========================================================

@router.post("/auth/register")
def register(data: RegisterRequest):

    user_id = data.user_id.strip()
    password = data.password.strip()

    # validation
    if len(user_id) < 3:
        raise HTTPException(
            status_code=400,
            detail="User ID too short"
        )

    if len(password) < 4:
        raise HTTPException(
            status_code=400,
            detail="Password too short"
        )

    result = auth.register(db, user_id, password)

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return {
        "status": "success",
        "message": "User registered successfully"
    }


# =========================================================
# LOGIN
# =========================================================

@router.post("/auth/login")
def login(data: LoginRequest):

    user_id = data.user_id.strip()
    password = data.password.strip()

    result = auth.login(db, user_id, password)

    if "error" in result:
        raise HTTPException(
            status_code=401,
            detail=result["error"]
        )

    return {
        "status": "success",
        "token": result["token"],
        "user_id": user_id
    }