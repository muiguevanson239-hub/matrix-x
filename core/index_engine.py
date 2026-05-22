import time
from collections import defaultdict


class IndexEngine:

    def __init__(self, db, embedder):

        self.db = db
        self.embedder = embedder

        # keyword index
        self.inverted_index = defaultdict(set)

        # vector cache index
        self.vector_index = {}

    # -----------------------------------------
    # BUILD INDEX
    # -----------------------------------------
    def build_index(self):

        for node_id, node in self.db.nodes.items():

            content = node.get("content", "")

            # keyword indexing
            for word in content.lower().split():
                self.inverted_index[word].add(node_id)

            # vector indexing (cache embeddings)
            self.vector_index[node_id] = self.embedder.embed(content)

    # -----------------------------------------
    # UPDATE SINGLE NODE INDEX
    # -----------------------------------------
    def index_node(self, node_id, node):

        content = node.get("content", "")

        for word in content.lower().split():
            self.inverted_index[word].add(node_id)

        self.vector_index[node_id] = self.embedder.embed(content)

    # -----------------------------------------
    # FAST KEYWORD SEARCH
    # -----------------------------------------
    def keyword_search(self, query):

        words = query.lower().split()

        results = set()

        for w in words:
            results.update(self.inverted_index.get(w, set()))

        return list(results)

    # -----------------------------------------
    # FAST VECTOR LOOKUP
    # -----------------------------------------
    def get_vector(self, node_id):

        return self.vector_index.get(node_id)

    # -----------------------------------------
    # STATS
    # -----------------------------------------
    def stats(self):

        return {
            "indexed_nodes": len(self.vector_index),
            "keywords": len(self.inverted_index)
        }