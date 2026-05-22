import time
import numpy as np
from sentence_transformers import SentenceTransformer


class RetrievalEngine:

    def __init__(self, db):

        self.db = db

        # lightweight embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # cache embeddings for speed
        self.cache = {}

    # -----------------------------------------
    # EMBEDDING
    # -----------------------------------------
    def embed(self, text):

        if text in self.cache:
            return self.cache[text]

        vec = self.model.encode(text)
        self.cache[text] = vec

        return vec

    # -----------------------------------------
    # SIMILARITY
    # -----------------------------------------
    def similarity(self, v1, v2):

        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return np.dot(v1, v2) / (norm1 * norm2)

    # -----------------------------------------
    # HYBRID SCORING
    # -----------------------------------------
    def score(self, query_vec, node):

        content = node.get("content", "")
        node_vec = self.embed(content)

        semantic = self.similarity(query_vec, node_vec)

        importance = node.get("importance", 0.5)
        usage = node.get("usage_count", 0)

        recency = 1 / (1 + (time.time() - node.get("last_accessed", time.time())))

        return (semantic * 0.6) + (importance * 0.2) + (usage * 0.1) + (recency * 0.1)

    # -----------------------------------------
    # SEARCH ENGINE
    # -----------------------------------------
    def search(self, query, top_k=5):

        query_vec = self.embed(query)

        results = []

        for node_id, node in self.db.nodes.items():

            score = self.score(query_vec, node)

            results.append({
                "id": node_id,
                "score": score,
                "node": node
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_k]

    # -----------------------------------------
    # CONTEXT BUILDER
    # -----------------------------------------
    def context(self, query, top_k=5):

        results = self.search(query, top_k)

        return [r["node"] for r in results]