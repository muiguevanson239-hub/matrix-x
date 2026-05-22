import time


class IntelligentDB:

    def __init__(self):

        # main storage
        self.nodes = {}

        # relationship graph
        self.edges = {}

    # -----------------------------------------
    # INSERT NODE
    # -----------------------------------------
    def insert(self, node):

        node_id = node["id"]

        node.setdefault("importance", 0.5)
        node.setdefault("usage_count", 0)
        node.setdefault("last_accessed", time.time())
        node.setdefault("relations", [])

        self.nodes[node_id] = node

    # -----------------------------------------
    # CONNECT NODES (GRAPH RELATIONSHIP)
    # -----------------------------------------
    def link(self, node_a, node_b, weight=1.0):

        self.edges.setdefault(node_a, [])
        self.edges[node_a].append({
            "target": node_b,
            "weight": weight
        })

    # -----------------------------------------
    # GET NODE
    # -----------------------------------------
    def get(self, node_id):

        node = self.nodes.get(node_id)

        if node:
            node["usage_count"] += 1
            node["last_accessed"] = time.time()

        return node

    # -----------------------------------------
    # SEARCH (SEMANTIC PLACEHOLDER)
    # -----------------------------------------
    def search(self, query_func):

        # query_func = external embedding similarity function
        results = []

        for node_id, node in self.nodes.items():

            score = query_func(node)

            results.append((score, node))

        results.sort(key=lambda x: x[0], reverse=True)

        return results

    # -----------------------------------------
    # CONTEXT BUILDER
    # -----------------------------------------
    def context(self, node_ids):

        return [self.nodes[nid] for nid in node_ids if nid in self.nodes]