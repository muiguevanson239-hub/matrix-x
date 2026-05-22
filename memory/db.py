import time
from core.redis_client import RedisClient


class Database:

    def __init__(self):

        # =====================================================
        # PRIMARY STORAGE (REDIS)
        # =====================================================

        self.redis = RedisClient()

    # =========================================================
    # USER SYSTEM
    # =========================================================

    def create_user(self, user_id, password_hash):

        key = f"user:{user_id}"

        if self.redis.exists(key):
            return False

        self.redis.hset(key, "user_id", user_id)
        self.redis.hset(key, "password", password_hash)
        self.redis.hset(key, "plan", "FREE")
        self.redis.hset(key, "created_at", str(time.time()))

        return True

    def get_user(self, user_id):

        key = f"user:{user_id}"

        if not self.redis.exists(key):
            return None

        return self.redis.hgetall(key)

    # =========================================================
    # PLAN SYSTEM
    # =========================================================

    def update_plan(self, user_id, plan):

        key = f"user:{user_id}"

        if not self.redis.exists(key):
            return False

        self.redis.hset(key, "plan", plan)
        self.redis.hset(key, "updated_at", str(time.time()))

        return True

    # =========================================================
    # MEMORY SYSTEM
    # =========================================================

    def add_memory(self, user_id, content, importance=0.5):

        key = f"memory:{user_id}"

        memory_item = {
            "content": content,
            "importance": importance,
            "timestamp": time.time()
        }

        existing = self.redis.get(key)

        if not existing:
            existing = []

        if isinstance(existing, str):
            existing = []

        existing.append(memory_item)

        self.redis.set(key, existing)

        return True

    def get_memory(self, user_id):

        key = f"memory:{user_id}"

        data = self.redis.get(key)

        if not data:
            return []

        if isinstance(data, str):
            return []

        return data

    # =========================================================
    # SESSION SYSTEM
    # =========================================================

    def create_session(self, session_id, user_id):

        key = f"session:{session_id}"

        self.redis.hset(key, "user_id", user_id)
        self.redis.hset(key, "created_at", str(time.time()))

        return True

    def get_session(self, session_id):

        key = f"session:{session_id}"

        if not self.redis.exists(key):
            return None

        return self.redis.hgetall(key)

    # =========================================================
    # CHAT HISTORY (OPTIONAL EXTENSION)
    # =========================================================

    def add_message(self, session_id, role, message):

        key = f"chat:{session_id}"

        chat = self.redis.get(key)

        if not chat:
            chat = []

        if isinstance(chat, str):
            chat = []

        chat.append({
            "role": role,
            "message": message,
            "timestamp": time.time()
        })

        self.redis.set(key, chat)

        return True

    def get_chat(self, session_id):

        key = f"chat:{session_id}"

        data = self.redis.get(key)

        if not data:
            return []

        if isinstance(data, str):
            return []

        return data

    # =========================================================
    # ADMIN HELPERS (FUTURE SaaS CONTROL)
    # =========================================================

    def get_all_users(self):

        # WARNING: simple scan (not for huge scale yet)
        keys = self.redis.client.keys("user:*")

        return [self.redis.hgetall(k) for k in keys]