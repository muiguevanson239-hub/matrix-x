from fastapi import APIRouter, Request
from memory.db import Database

router = APIRouter()
db = Database()


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):

    payload = await request.json()

    if payload["type"] == "checkout.session.completed":

        session = payload["data"]["object"]

        user_id = session["metadata"]["user_id"]
        plan = session["metadata"]["plan"]

        db.update_plan(user_id, plan)

    return {"status": "ok"}