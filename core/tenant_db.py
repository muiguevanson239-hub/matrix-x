import time
from collections import defaultdict


class TenantDB:

    def __init__(self):

        # tenant → nodes
        self.data = defaultdict(dict)

        # tenant → metadata
        self.meta = defaultdict(lambda: {
            "created_at": time.time(),
            "requests": 0
        })

    # -----------------------------------------
    # CREATE TENANT
    # -----------------------------------------
    def create_tenant(self, tenant_id):

        if tenant_id not in self.data:

            self.data[tenant_id] = {}
            self.meta[tenant_id] = {
                "created_at": time.time(),
                "requests": 0
            }

        return tenant_id

    # -----------------------------------------
    # INSERT NODE
    # -----------------------------------------
    def insert(self, tenant_id, node):

        self.create_tenant(tenant_id)

        node_id = node["id"]
        self.data[tenant_id][node_id] = node

    # -----------------------------------------
    # GET NODE
    # -----------------------------------------
    def get(self, tenant_id, node_id):

        return self.data[tenant_id].get(node_id)

    # -----------------------------------------
    # GET ALL NODES
    # -----------------------------------------
    def all(self, tenant_id):

        return self.data[tenant_id]

    # -----------------------------------------
    # TRACK USAGE
    # -----------------------------------------
    def track(self, tenant_id):

        self.meta[tenant_id]["requests"] += 1

    # -----------------------------------------
    # STATS
    # -----------------------------------------
    def stats(self, tenant_id):

        return {
            "tenant": tenant_id,
            "nodes": len(self.data[tenant_id]),
            "requests": self.meta[tenant_id]["requests"]
        }