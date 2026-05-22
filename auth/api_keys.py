import uuid
import hashlib
import time


class APIKeyManager:

    def __init__(self):

        # In production:
        # move this to DB or Redis
        self.keys = {}

        # Default limits by plan
        self.plan_limits = {
            "FREE": 30,
            "STARTER": 100,
            "PRO": 500,
            "ELITE": 1500,
            "BUSINESS": 5000,
            "ENTERPRISE": 20000,
            "LEGEND": 999999
        }

    # =====================================================
    # HASH KEY
    # =====================================================

    def _hash_key(self, key):

        return hashlib.sha256(
            key.encode()
        ).hexdigest()

    # =====================================================
    # CREATE API KEY
    # =====================================================

    def create_key(self, user_id, plan="FREE"):

        raw_key = f"mx_{uuid.uuid4().hex}"

        hashed = self._hash_key(raw_key)

        self.keys[hashed] = {
            "user_id": user_id,
            "plan": plan,
            "created_at": time.time(),
            "requests": 0,
            "window_start": time.time(),
            "active": True,
            "last_used": None,
            "total_requests": 0
        }

        # RETURN RAW KEY ONLY ONCE
        return raw_key

    # =====================================================
    # VALIDATE API KEY
    # =====================================================

    def validate(self, raw_key):

        hashed = self._hash_key(raw_key)

        data = self.keys.get(hashed)

        if not data:
            return False, "Invalid API key"

        if not data["active"]:
            return False, "API key disabled"

        now = time.time()

        # RESET WINDOW EVERY 60 SECONDS
        if now - data["window_start"] > 60:

            data["window_start"] = now
            data["requests"] = 0

        limit = self.plan_limits.get(
            data["plan"],
            30
        )

        # RATE LIMIT
        if data["requests"] >= limit:

            return False, (
                f"Rate limit exceeded "
                f"({limit} requests/min)"
            )

        return True, data

    # =====================================================
    # TRACK REQUEST
    # =====================================================

    def track(self, raw_key):

        hashed = self._hash_key(raw_key)

        if hashed not in self.keys:
            return

        self.keys[hashed]["requests"] += 1
        self.keys[hashed]["total_requests"] += 1
        self.keys[hashed]["last_used"] = time.time()

    # =====================================================
    # DISABLE KEY
    # =====================================================

    def disable_key(self, raw_key):

        hashed = self._hash_key(raw_key)

        if hashed in self.keys:
            self.keys[hashed]["active"] = False

    # =====================================================
    # ENABLE KEY
    # =====================================================

    def enable_key(self, raw_key):

        hashed = self._hash_key(raw_key)

        if hashed in self.keys:
            self.keys[hashed]["active"] = True

    # =====================================================
    # RESET RATE LIMIT WINDOW
    # =====================================================

    def reset_key(self, raw_key):

        hashed = self._hash_key(raw_key)

        if hashed in self.keys:

            self.keys[hashed]["requests"] = 0
            self.keys[hashed]["window_start"] = time.time()

    # =====================================================
    # GET STATS
    # =====================================================

    def stats(self, raw_key):

        hashed = self._hash_key(raw_key)

        if hashed not in self.keys:
            return None

        data = self.keys[hashed]

        return {
            "user_id": data["user_id"],
            "plan": data["plan"],
            "created_at": data["created_at"],
            "last_used": data["last_used"],
            "total_requests": data["total_requests"],
            "active": data["active"]
        }