import time


class SmartLayer:

    def __init__(self, memory_store):
        self.memory = memory_store

    # ---------------------------------
    # SCORE MEMORY INTELLIGENCE
    # ---------------------------------
    def score_node(self, node):

        importance = node.get("importance", 0.5)
        usage = node.get("usage_count", 0)
        last_used = node.get("last_used", time.time())

        # recency decay (newer = better)
        recency = 1 / (1 + (time.time() - last_used) / 10000)

        score = (importance * 0.5) + (usage * 0.3) + (recency * 0.2)

        return score

    # ---------------------------------
    # ENHANCED CONTEXT SORTING
    # ---------------------------------
    def rank_memory(self, memory_list):

        ranked = sorted(
            memory_list,
            key=lambda x: self.score_node(x),
            reverse=True
        )

        return ranked

    # ---------------------------------
    # INTENT BOOSTER (SMALL UPGRADE)
    # ---------------------------------
    def detect_intent_weight(self, query):

        q = query.lower()

        if "urgent" in q or "important" in q:
            return 1.2

        if "why" in q:
            return 1.1

        return 1.0