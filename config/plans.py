# =========================================================
# MATRIX X — PLAN SYSTEM (SAAS CORE)
# =========================================================

PLANS = {
    "FREE": {
        "tier": 0,
        "price": 0,
        "memory_limit": 20,
        "streaming": False,
        "priority": 0,
        "features": [
            "chat"
        ],
        "limits": {
            "requests_per_minute": 30,
            "sessions": 1
        }
    },

    "STARTER": {
        "tier": 1,
        "price": 5,
        "memory_limit": 50,
        "streaming": False,
        "priority": 1,
        "features": [
            "chat",
            "memory"
        ],
        "limits": {
            "requests_per_minute": 100,
            "sessions": 3
        }
    },

    "PRO": {
        "tier": 2,
        "price": 15,
        "memory_limit": 200,
        "streaming": True,
        "priority": 2,
        "features": [
            "chat",
            "memory",
            "streaming"
        ],
        "limits": {
            "requests_per_minute": 300,
            "sessions": 10
        }
    },

    "ELITE": {
        "tier": 3,
        "price": 29,
        "memory_limit": 500,
        "streaming": True,
        "priority": 3,
        "features": [
            "chat",
            "memory",
            "streaming",
            "priority_ai"
        ],
        "limits": {
            "requests_per_minute": 1000,
            "sessions": 30
        }
    },

    "BUSINESS": {
        "tier": 4,
        "price": 79,
        "memory_limit": 2000,
        "streaming": True,
        "priority": 4,
        "features": [
            "chat",
            "memory",
            "streaming",
            "team",
            "analytics"
        ],
        "limits": {
            "requests_per_minute": 5000,
            "sessions": 100
        }
    },

    "ENTERPRISE": {
        "tier": 5,
        "price": 199,
        "memory_limit": 10000,
        "streaming": True,
        "priority": 5,
        "features": [
            "api",
            "team",
            "analytics",
            "dedicated_support"
        ],
        "limits": {
            "requests_per_minute": 20000,
            "sessions": 1000
        }
    },

    "LEGEND": {
        "tier": 6,
        "price": 499,
        "memory_limit": -1,
        "streaming": True,
        "priority": 999,
        "features": [
            "everything"
        ],
        "limits": {
            "requests_per_minute": -1,
            "sessions": -1
        }
    }
}


# =========================================================
# HELPER FUNCTIONS (IMPORTANT FOR ENGINE)
# =========================================================

def get_plan(name: str):
    return PLANS.get(name.upper(), PLANS["FREE"])


def can_use_feature(plan: str, feature: str):
    p = get_plan(plan)
    return "everything" in p["features"] or feature in p["features"]


def upgrade_path(current_plan: str):
    return sorted(PLANS.keys(), key=lambda x: PLANS[x]["tier"])