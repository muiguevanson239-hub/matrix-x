import time
import uuid


class APIGateway:

    def __init__(self):

        self.keys = {}

        self.rate_limit = 60  # requests per minute

    # -----------------------------------------
    # CREATE API KEY
    # -----------------------------------------
    def create_key(self, user_id):

        key = str(uuid.uuid4())

        self.keys[key] = {
            "user_id": user_id,
            "requests": 0,
            "window_start": time.time()
        }

        return key

    # -----------------------------------------
    # VALIDATE KEY
    # -----------------------------------------
    def validate(self, key):

        data = self.keys.get(key)

        if not data:
            return False, "Invalid API key"

        now = time.time()

        # reset window every 60s
        if now - data["window_start"] > 60:
            data["window_start"] = now
            data["requests"] = 0

        if data["requests"] >= self.rate_limit:
            return False, "Rate limit exceeded"

        return True, data["user_id"]

    # -----------------------------------------
    # TRACK USAGE
    # -----------------------------------------
    def track(self, key):

        if key in self.keys:
            self.keys[key]["requests"] += 1

    # -----------------------------------------
    # STATS
    # -----------------------------------------
    def stats(self):

        return {
            "total_keys": len(self.keys)
        }