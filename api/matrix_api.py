from fastapi import FastAPI, Header
from pydantic import BaseModel

from core.bootstrap import MatrixX

app = FastAPI(title="Matrix X Infrastructure API")

# -------------------------
# INIT SYSTEM (ONE INSTANCE)
# -------------------------
system = MatrixX()


# -------------------------
# REQUEST MODEL
# -------------------------
class QueryRequest(BaseModel):
    tenant_id: str
    query: str


# -------------------------
# MAIN QUERY ENDPOINT
# -------------------------
@app.post("/v1/query")
def query(req: QueryRequest, x_api_key: str = Header(None)):

    if not x_api_key:
        return {"error": "missing API key"}

    result = system.handle(
        api_key=x_api_key,
        tenant_id=req.tenant_id,
        query=req.query
    )

    return result


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/health")
def health():

    return {
        "status": "online",
        "system": "Matrix X",
        "version": "1.0"
    }


# -------------------------
# CREATE API KEY (DEV ONLY)
# -------------------------
@app.post("/v1/create-key")
def create_key(user_id: str):

    key = system.gateway.create_key(user_id)

    return {
        "api_key": key
    }