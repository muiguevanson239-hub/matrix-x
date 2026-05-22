from fastapi import APIRouter
from auth.auth import AuthSystem
from config.plans import PLANS, get_plan
from core.redis_client import RedisClient

router = APIRouter()

auth = AuthSystem()
redis = RedisClient()


# =========================================================
# GET MEMORY (USER-SAFE)
# =========================================================

@router.get("/memory")
def memory(token: str):

    user_id = auth.authenticate(token)

    if not user_id:

        return {"error": "invalid token"}

    # Redis memory key
    key = f"memory:{user_id}"

    memory_data = redis.get(key)

    if not memory_data:

        return {"memory": []}

    return {
        "user_id": user_id,
        "memory": memory_data
    }


# =========================================================
# UPGRADE PLAN (SECURE)
# =========================================================

@router.post("/upgrade")
def upgrade(token: str, plan: str):

    user_id = auth.authenticate(token)

    if not user_id:

        return {"error": "invalid token"}

    plan = plan.upper()

    # VALIDATE PLAN EXISTS
    if plan not in PLANS:

        return {
            "error": "invalid plan"
        }

    # GET CURRENT USER DATA
    user_key = f"user:{user_id}"

    user_data = redis.hgetall(user_key)

    current_plan = user_data.get("plan", "FREE")

    # PREVENT DOWNGRADES WITHOUT LOGIC
    if get_plan(plan)["tier"] < get_plan(current_plan)["tier"]:

        return {
            "error": "downgrade not allowed"
        }

    # UPDATE USER PLAN
    redis.hset(user_key, "plan", plan)

    return {
        "status": "upgraded",
        "user_id": user_id,
        "new_plan": plan
    }