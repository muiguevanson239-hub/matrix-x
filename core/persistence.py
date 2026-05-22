import json
import os
import time


class PersistenceEngine:

    def __init__(self, path="matrix_storage.json"):

        self.path = path

        # in-memory state
        self.state = {
            "nodes": {},
            "tenants": {},
            "api_keys": {},
            "meta": {
                "created_at": time.time()
            }
        }

        self.load()

    # -----------------------------------------
    # LOAD FROM DISK
    # -----------------------------------------
    def load(self):

        if not os.path.exists(self.path):
            return

        try:
            with open(self.path, "r") as f:
                self.state = json.load(f)

        except Exception:
            print("[Persistence] Failed to load state, starting fresh")

    # -----------------------------------------
    # SAVE TO DISK
    # -----------------------------------------
    def save(self):

        try:
            with open(self.path, "w") as f:
                json.dump(self.state, f, indent=2)

        except Exception as e:
            print("[Persistence] Save error:", e)

    # -----------------------------------------
    # NODES
    # -----------------------------------------
    def set_node(self, node_id, node):

        self.state["nodes"][node_id] = node
        self.save()

    def get_node(self, node_id):

        return self.state["nodes"].get(node_id)

    # -----------------------------------------
    # TENANTS
    # -----------------------------------------
    def set_tenant(self, tenant_id, data):

        self.state["tenants"][tenant_id] = data
        self.save()

    def get_tenant(self, tenant_id):

        return self.state["tenants"].get(tenant_id)

    # -----------------------------------------
    # API KEYS
    # -----------------------------------------
    def set_key(self, key, data):

        self.state["api_keys"][key] = data
        self.save()

    def get_key(self, key):

        return self.state["api_keys"].get(key)

    # -----------------------------------------
    # STATS
    # -----------------------------------------
    def stats(self):

        return {
            "nodes": len(self.state["nodes"]),
            "tenants": len(self.state["tenants"]),
            "api_keys": len(self.state["api_keys"])
        }