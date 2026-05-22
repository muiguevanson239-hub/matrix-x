import time


class Orchestrator:

    def __init__(self, gateway, tenant_db, query_engine):

        self.gateway = gateway
        self.tenant_db = tenant_db
        self.query_engine = query_engine

    # -----------------------------------------
    # MAIN ENTRY POINT
    # -----------------------------------------
    def handle(self, api_key, tenant_id, query):

        start = time.time()

        # STEP 1: validate API key
        valid, result = self.gateway.validate(api_key)

        if not valid:
            return {"error": result}

        # STEP 2: ensure tenant exists
        self.tenant_db.create_tenant(tenant_id)

        # STEP 3: track usage
        self.gateway.track(api_key)
        self.tenant_db.track(tenant_id)

        # STEP 4: run query engine
        response = self.query_engine.query(query)

        # STEP 5: format unified response
        return {
            "tenant": tenant_id,
            "query": query,
            "results": response["results"],
            "took_ms": (time.time() - start) * 1000,
            "status": "success"
        }