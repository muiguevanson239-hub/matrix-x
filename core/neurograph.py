from sentence_transformers import SentenceTransformer
import numpy as np


class NeuroGraph:

    def __init__(self, memory):

        self.memory = memory

        # Lightweight but strong embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # =====================================================
        # EMBEDDING CACHE (CRITICAL UPGRADE)
        # =====================================================

        self.embedding_cache = {}

    # =========================================================
    # EMBEDDING WITH CACHE
    # =========================================================

    def _vectorize(self, text):

        if text in self.embedding_cache:

            return self.embedding_cache[text]

        vector = self.model.encode(text)

        self.embedding_cache[text] = vector

        return vector

    # =========================================================
    # COSINE SIMILARITY
    # =========================================================

    def _similarity(self, v1, v2):

        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return np.dot(v1, v2) / (norm1 * norm2)

    # =========================================================
    # SEARCH MEMORY (OPTIMIZED)
    # =========================================================

    def search(self, query, top_k=5):

        query_vec = self._vectorize(query)

        results = []

        # iterate memory once
        for node_id, node in self.memory.items():

            content = node.get("content", "")

            node_vec = self._vectorize(content)

            score = self._similarity(query_vec, node_vec)

            results.append((score, node))

        results.sort(key=lambda x: x[0], reverse=True)

        return results[:top_k]

    # =========================================================
    # CONTEXT BUILDER (IMPROVED)
    # =========================================================

    def build_context(self, query, top_k=5):

        results = self.search(query, top_k)

        context = []

        for score, node in results:

            context.append({
                "id": node.get("id"),
                "content": node.get("content"),
                "importance": node.get("importance", 0),
                "score": float(score)
            })

        return context

    # =========================================================
    # CACHE MANAGEMENT (NEW)
    # =========================================================

    def clear_cache(self):

        self.embedding_cache.clear()

    # =========================================================
    # MEMORY STATS (NEW)
    # =========================================================

    def stats(self):

        return {
            "memory_nodes": len(self.memory),
            "cached_embeddings": len(self.embedding_cache)
        }