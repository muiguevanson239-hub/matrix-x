from fastapi import APIRouter
from auth.auth import AuthSystem
from core.stripe_client import StripeClient

router = APIRouter()
auth = AuthSystem()
stripe_client = StripeClient()


PRICE_MAP = {
    "STARTER": "price_start",
    "PRO": "price_pro",
    "ELITE": "price_elite"
}


@router.post("/billing/checkout")
def checkout(token: str, plan: str, country: str = "KE"):

    user_id = auth.authenticate(token)

    if not user_id:
        return {"error": "invalid token"}

    plan = plan.upper()

    if plan not in PRICE_MAP:
        return {"error": "invalid plan"}

    url = stripe_client.create_checkout(
        user_id=user_id,
        plan=plan,
        price_id=PRICE_MAP[plan]
    )

    return {
        "status": "success",
        "checkout": url
    }