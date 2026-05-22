import os
import json
import redis


class RedisClient:

    def __init__(self):

        # =====================================================
        # CONNECTION CONFIG
        # =====================================================

        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.db = int(os.getenv("REDIS_DB", 0))

        # Create connection pool (IMPORTANT for performance)
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )

    # =========================================================
    # SET VALUE
    # =========================================================

    def set(self, key, value, ex=None):

        """
        ex = expiration time in seconds
        """

        if isinstance(value, (dict, list)):

            value = json.dumps(value)

        return self.client.set(key, value, ex=ex)

    # =========================================================
    # GET VALUE
    # =========================================================

    def get(self, key):

        value = self.client.get(key)

        if value is None:
            return None

        try:
            return json.loads(value)

        except Exception:
            return value

    # =========================================================
    # DELETE KEY
    # =========================================================

    def delete(self, key):

        return self.client.delete(key)

    # =========================================================
    # EXISTS CHECK
    # =========================================================

    def exists(self, key):

        return self.client.exists(key) == 1

    # =========================================================
    # EXPIRE KEY
    # =========================================================

    def expire(self, key, seconds):

        return self.client.expire(key, seconds)

    # =========================================================
    # INCREMENT (FOR RATE LIMITING)
    # =========================================================

    def incr(self, key, amount=1):

        return self.client.incr(key, amount)

    # =========================================================
    # HASH OPERATIONS (FOR USERS / SESSIONS)
    # =========================================================

    def hset(self, name, key, value):

        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        return self.client.hset(name, key, value)

    def hget(self, name, key):

        value = self.client.hget(name, key)

        if value is None:
            return None

        try:
            return json.loads(value)

        except Exception:
            return value

    def hgetall(self, name):

        data = self.client.hgetall(name)

        parsed = {}

        for k, v in data.items():

            try:
                parsed[k] = json.loads(v)
            except Exception:
                parsed[k] = v

        return parsed

    # =========================================================
    # LIST OPERATIONS (FOR LOGS / CHAT HISTORY)
    # =========================================================

    def lpush(self, key, value):

        if isinstance(value, (dict, list)):

            value = json.dumps(value)

        return self.client.lpush(key, value)

    def lrange(self, key, start=0, end=-1):

        data = self.client.lrange(key, start, end)

        parsed = []

        for item in data:

            try:
                parsed.append(json.loads(item))
            except Exception:
                parsed.append(item)

        return parsed

    # =========================================================
    # HEALTH CHECK
    # =========================================================

    def ping(self):

        return self.client.ping()