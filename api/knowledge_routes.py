from fastapi import APIRouter
from core.intelligent_db import IntelligentDB
from core.retrieval_engine import RetrievalEngine

router = APIRouter()

db = IntelligentDB()
retrieval = RetrievalEngine(db)


# =========================================================
# INSERT NODE (WRITE API)
# =========================================================
@router.post("/knowledge/insert")
def insert_node(node: dict):

    if "id" not in node or "content" not in node:
        return {"error": "id and content required"}

    db.insert(node)

    return {
        "status": "inserted",
        "id": node["id"]
    }


# =========================================================
# SEARCH KNOWLEDGE (READ API)
# =========================================================
@router.get("/knowledge/search")
def search(q: str, limit: int = 5):

    results = retrieval.search(q, top_k=limit)

    return {
        "query": q,
        "results": results
    }


# =========================================================
# GET CONTEXT (AI / APPS USE THIS)
# =========================================================
@router.get("/knowledge/context")
def context(q: str, limit: int = 5):

    nodes = retrieval.context(q, top_k=limit)

    return {
        "query": q,
        "context": nodes
    }


# =========================================================
# LINK NODES (GRAPH RELATIONSHIP)
# =========================================================
@router.post("/knowledge/link")
def link(data: dict):

    a = data.get("a")
    b = data.get("b")
    weight = data.get("weight", 1.0)

    if not a or not b:
        return {"error": "missing nodes"}

    db.link(a, b, weight)

    return {
        "status": "linked",
        "from": a,
        "to": b
    }