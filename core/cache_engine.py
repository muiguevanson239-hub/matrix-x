import time


class CacheEngine:

    def __init__(self, ttl=300):

        # TTL in seconds
        self.ttl = ttl

        # caches
        self.query_cache = {}
        self.node_cache = {}
        self.embedding_cache = {}

    # -----------------------------------------
    # GENERAL CACHE VALIDATION
    # -----------------------------------------
    def _valid(self, entry):

        if not entry:
            return False

        return (time.time() - entry["time"]) < self.ttl

    # -----------------------------------------
    # QUERY CACHE
    # -----------------------------------------
    def get_query(self, key):

        entry = self.query_cache.get(key)

        if self._valid(entry):
            return entry["value"]

        return None

    def set_query(self, key, value):

        self.query_cache[key] = {
            "value": value,
            "time": time.time()
        }

    # -----------------------------------------
    # NODE CACHE
    # -----------------------------------------
    def get_node(self, node_id):

        entry = self.node_cache.get(node_id)

        if self._valid(entry):
            return entry["value"]

        return None

    def set_node(self, node_id, node):

        self.node_cache[node_id] = {
            "value": node,
            "time": time.time()
        }

    # -----------------------------------------
    # EMBEDDING CACHE
    # -----------------------------------------
    def get_embedding(self, text):

        entry = self.embedding_cache.get(text)

        if self._valid(entry):
            return entry["value"]

        return None

    def set_embedding(self, text, vector):

        self.embedding_cache[text] = {
            "value": vector,
            "time": time.time()
        }

    # -----------------------------------------
    # STATS
    # -----------------------------------------
    def stats(self):

        return {
            "query_cache": len(self.query_cache),
            "node_cache": len(self.node_cache),
            "embedding_cache": len(self.embedding_cache)
        }