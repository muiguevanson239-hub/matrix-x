from core.retrieval_engine import RetrievalEngine


class MatrixX:

    def __init__(self, memory=None):

        self.memory = memory or {}
        self.engine = RetrievalEngine()

    # -------------------------
    # LOAD MEMORY
    # -------------------------
    def load_memory(self, memory_dict):
        self.memory = memory_dict

    # -------------------------
    # QUERY SYSTEM
    # -------------------------
    def query(self, text: str):

        results = self.engine.search_memory(self.memory, text)

        return {
            "query": text,
            "results": results,
            "status": "ok"
        }

    # -------------------------
    # HEALTH CHECK
    # -------------------------
    def health(self):

        return {
            "status": "online",
            "memory_size": len(self.memory)
        }