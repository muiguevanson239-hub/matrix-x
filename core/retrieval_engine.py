# core/bootstrap.py

from core.retrieval_engine import RetrievalEngine


class MatrixX:

    def __init__(self, memory=None):
        """
        Safe bootstrap layer for Matrix X.
        Works on free-tier deployment (no ML dependencies).
        """

        self.memory = memory or {}

        # -------------------------
        # CORE ENGINE
        # -------------------------
        self.retrieval = RetrievalEngine()

        # -------------------------
        # SYSTEM STATE
        # -------------------------
        self.version = "1.0-stable"
        self.status = "initializing"

        # -------------------------
        # OPTIONAL MODULES (SAFE INIT)
        # -------------------------
        self.modules = {}

        self._initialize_system()

    # =========================================================
    # SYSTEM INIT
    # =========================================================

    def _initialize_system(self):

        try:
            self.status = "online"

        except Exception as e:
            self.status = "degraded"
            print("[MatrixX Bootstrap Error]", str(e))

    # =========================================================
    # MEMORY ACCESS LAYER
    # =========================================================

    def load_memory(self, memory_dict):
        """
        Inject memory safely from DB or Redis layer
        """

        if not isinstance(memory_dict, dict):
            return

        self.memory = memory_dict

    # =========================================================
    # QUERY PIPELINE
    # =========================================================

    def query(self, text):
        """
        Main entry point for Matrix X reasoning.
        Lightweight retrieval only (no ML models).
        """

        try:
            context = self.retrieval.search_memory(self.memory, text)

            return {
                "query": text,
                "context": context,
                "status": "success",
                "engine": "lightweight-retrieval"
            }

        except Exception as e:

            return {
                "query": text,
                "error": str(e),
                "status": "failed"
            }

    # =========================================================
    # SYSTEM HEALTH
    # =========================================================

    def health(self):

        return {
            "status": self.status,
            "version": self.version,
            "memory_nodes": len(self.memory)
        }