from fastapi import APIRouter, Request
from memory.db import Database
from auth.auth import AuthSystem

router = APIRouter()

db = Database()
auth = AuthSystem()


# =========================================================
# BILLING WEBHOOK (MULTI-PROVIDER READY)
# =========================================================

@router.post("/billing/webhook/{provider}")
async def billing_webhook(provider: str, request: Request):

    payload = await request.json()

    provider = provider.lower()

    # =========================
    # STRIPE WEBHOOK
    # =========================
    if provider == "stripe":

        event_type = payload.get("type")

        if event_type == "checkout.session.completed":

            session = payload["data"]["object"]

            user_id = session["metadata"]["user_id"]
            plan = session["metadata"]["plan"]

            db.update_plan(user_id, plan)

            return {"status": "stripe_success", "user_id": user_id}

    # =========================
    # FLUTTERWAVE WEBHOOK
    # =========================
    if provider == "flutterwave":

        data = payload.get("data", {})

        if data.get("status") == "successful":

            user_id = data.get("meta", {}).get("user_id")
            plan = data.get("meta", {}).get("plan")

            if user_id and plan:
                db.update_plan(user_id, plan)

            return {"status": "flutterwave_success"}

    return {
        "status": "ignored",
        "provider": provider
    }