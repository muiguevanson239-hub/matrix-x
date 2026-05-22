class MatrixXEngine:

    def __init__(self, config=None):

        # allow future scaling
        self.config = config or {}

        self.memory = {}
        self.links = {}

        # optional settings
        self.name = self.config.get("name", "MatrixXEngine")
        self.debug = self.config.get("debug", False)

    # ---------------------------------
    # STORE MEMORY NODE
    # ---------------------------------
    def store(self, node):
        node_id = node["id"]
        self.memory[node_id] = node

    # ---------------------------------
    # GET MEMORY
    # ---------------------------------
    def get_memory(self, user_id=None):
        return list(self.memory.values())

    # ---------------------------------
    # ADAPT / LEARN
    # ---------------------------------
    def adapt(self, accessed_nodes):
        for node_id in accessed_nodes:
            if node_id in self.memory:
                self.memory[node_id]["usage_count"] = \
                    self.memory[node_id].get("usage_count", 0) + 1