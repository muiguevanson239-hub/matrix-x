from fastapi import FastAPI
from core.bootstrap import MatrixX

app = FastAPI()

engine = MatrixX()


@app.get("/health")
def health():
    return engine.health()


@app.post("/query")
def query(payload: dict):
    text = payload.get("text", "")
    return engine.query(text)