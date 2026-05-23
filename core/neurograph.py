import numpy as np
import hashlib


class NeuroGraph:

    def __init__(self, memory):
        self.memory = memory

    # -------------------------
    # LIGHTWEIGHT VECTOR
    # -------------------------
    def _vectorize(self, text):
        h = hashlib.md5(text.encode()).hexdigest()
        return np.array([int(h[i:i+2], 16) for i in range(0, 32, 2)])

    # -------------------------
    # COSINE SIMILARITY
    # -------------------------
    def _similarity(self, v1, v2):
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return np.dot(v1, v2) / (norm1 * norm2)

    # -------------------------
    # SEARCH MEMORY
    # -------------------------
    def search(self, query, top_k=5):

        query_vec = self._vectorize(query)
        results = []

        for node_id, node in self.memory.items():

            node_vec = self._vectorize(node["content"])
            score = self._similarity(query_vec, node_vec)

            results.append((score, node))

        results.sort(key=lambda x: x[0], reverse=True)

        return results[:top_k]

    # -------------------------
    # CONTEXT BUILDER
    # -------------------------
    def build_context(self, query, top_k=5):

        results = self.search(query, top_k)

        return [
            {
                "id": node["id"],
                "content": node["content"],
                "importance": node["importance"],
                "score": float(score)
            }
            for score, node in results
        ]