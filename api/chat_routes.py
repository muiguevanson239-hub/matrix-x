from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import uuid
import asyncio
import json

from memory.db import Database
from auth.auth import AuthSystem
from core.engine_singleton import engine
from core.plan_manager import PlanManager

router = APIRouter(
    tags=["Chat"]
)

db = Database()
auth = AuthSystem()
plans = PlanManager()


# =========================================================
# REQUEST MODELS
# =========================================================

class SendMessageRequest(BaseModel):
    token: str
    session_id: str
    message: str


class CreateSessionRequest(BaseModel):
    token: str


# =========================================================
# CREATE SESSION
# =========================================================

@router.post("/chat/session/create")
def create_session(data: CreateSessionRequest):

    user_id = auth.authenticate(data.token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    session_id = str(uuid.uuid4())

    db.create_session(session_id, user_id)

    return {
        "status": "success",
        "session_id": session_id
    }


# =========================================================
# SEND MESSAGE
# =========================================================

@router.post("/chat/send")
def send(data: SendMessageRequest):

    user_id = auth.authenticate(data.token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    message = data.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    if len(message) > 5000:
        raise HTTPException(
            status_code=400,
            detail="Message too large"
        )

    user = db.get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    plan = user["plan"]

    memory = db.get_memory(user_id)

    limit = plans.memory_limit(plan)

    if limit != -1 and len(memory) > limit:
        raise HTTPException(
            status_code=403,
            detail="Memory limit reached. Upgrade required."
        )

    # STORE USER MESSAGE
    db.add_message(data.session_id, "user", message)

    # ENGINE PROCESSING
    result = engine.process(
        message,
        user_id=user_id
    )

    reply = str(
        result.get("tool_result")
        or result.get("input")
        or "No response generated."
    )

    # STORE AI RESPONSE
    db.add_message(data.session_id, "ai", reply)

    return {
        "status": "success",
        "response": reply
    }


# =========================================================
# STREAM CHAT
# =========================================================

@router.post("/chat/stream")
async def stream(data: SendMessageRequest):

    user_id = auth.authenticate(data.token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    plan = user["plan"]

    if not plans.can_stream(plan):
        raise HTTPException(
            status_code=403,
            detail="Streaming unavailable in your plan"
        )

    message = data.message.strip()

    db.add_message(data.session_id, "user", message)

    result = engine.process(
        message,
        user_id=user_id
    )

    reply = str(
        result.get("tool_result")
        or result.get("input")
        or "No response generated."
    )

    async def generator():

        for char in reply:

            yield json.dumps({
                "token": char
            }) + "\n"

            await asyncio.sleep(0.01)

        db.add_message(data.session_id, "ai", reply)

    return StreamingResponse(
        generator(),
        media_type="text/plain"
    )


# =========================================================
# GET SESSION HISTORY
# =========================================================

@router.get("/chat/history/{session_id}")
def history(session_id: str, token: str):

    user_id = auth.authenticate(token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    messages = db.get_messages(session_id)

    return {
        "status": "success",
        "messages": messages
    }