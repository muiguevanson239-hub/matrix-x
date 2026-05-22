import time


class QueryEngine:

    def __init__(self, db, index_engine, retrieval_engine):

        self.db = db
        self.index = index_engine
        self.retrieval = retrieval_engine

    # -----------------------------------------
    # MAIN ENTRY POINT
    # -----------------------------------------
    def query(self, text, top_k=5):

        start = time.time()

        # STEP 1: keyword candidates (fast path)
        keyword_ids = set(self.index.keyword_search(text))

        # STEP 2: vector candidates (semantic path)
        vector_results = self.retrieval.search(text, top_k=top_k * 2)

        vector_ids = {r["id"] for r in vector_results}

        # STEP 3: merge candidates
        candidates = keyword_ids.union(vector_ids)

        scored = []

        query_vec = self.retrieval.embed(text)

        # STEP 4: score all candidates
        for node_id in candidates:

            node = self.db.get(node_id)
            if not node:
                continue

            # semantic score
            node_vec = self.retrieval.embed(node.get("content", ""))
            semantic = self.retrieval.similarity(query_vec, node_vec)

            # metadata boost
            importance = node.get("importance", 0.5)
            usage = node.get("usage_count", 0)

            recency = 1 / (1 + (time.time() - node.get("last_accessed", time.time())))

            final_score = (
                semantic * 0.6 +
                importance * 0.2 +
                usage * 0.1 +
                recency * 0.1
            )

            scored.append({
                "id": node_id,
                "score": final_score,
                "node": node
            })

        # STEP 5: sort results
        scored.sort(key=lambda x: x["score"], reverse=True)

        return {
            "query": text,
            "results": scored[:top_k],
            "took_ms": (time.time() - start) * 1000
        }