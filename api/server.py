from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import time

# =========================================================
# ENGINE
# =========================================================

from core.matrix_engine import MatrixXEngine

engine = MatrixXEngine()

# =========================================================
# ROUTES
# =========================================================

from api.auth_routes import router as auth_router
from api.chat_routes import router as chat_router
from api.billing_routes import router as billing_router
from dashboard.routes import router as dashboard_router

# OPTIONAL STRIPE WEBHOOK
try:
    from api.webhook import router as webhook_router
    WEBHOOKS_ENABLED = True
except:
    WEBHOOKS_ENABLED = False

# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="Matrix X",
    version="5.0"
)

# =========================================================
# ROUTERS
# =========================================================

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(billing_router)
app.include_router(dashboard_router, prefix="/dashboard")

if WEBHOOKS_ENABLED:
    app.include_router(webhook_router)

# =========================================================
# STATIC UI
# =========================================================

app.mount(
    "/ui",
    StaticFiles(directory="dashboard_ui", html=True),
    name="ui"
)

# =========================================================
# REQUEST MODELS
# =========================================================

class QueryRequest(BaseModel):
    query: str

# =========================================================
# RATE LIMITER
# =========================================================

RATE_LIMIT = 60
WINDOW = 60

request_log = {}


def check_rate_limit(ip):

    now = time.time()

    if ip not in request_log:
        request_log[ip] = []

    request_log[ip] = [
        t for t in request_log[ip]
        if now - t < WINDOW
    ]

    if len(request_log[ip]) >= RATE_LIMIT:
        return False

    request_log[ip].append(now)

    return True

# =========================================================
# MIDDLEWARE
# =========================================================

@app.middleware("http")
async def middleware(request: Request, call_next):

    ip = request.client.host

    if not check_rate_limit(ip):

        return JSONResponse(
            status_code=429,
            content={
                "status": "error",
                "message": "Too many requests"
            }
        )

    response = await call_next(request)

    response.headers["X-Powered-By"] = "Matrix X"
    response.headers["Cache-Control"] = "no-store"

    return response

# =========================================================
# ROOT
# =========================================================

@app.get("/")
def home():

    return {
        "status": "online",
        "service": "Matrix X",
        "version": "5.0",
        "ui": "/ui",
        "docs": "/docs"
    }

# =========================================================
# MAIN PROCESS ENDPOINT
# =========================================================

@app.post("/process")
def process(req: QueryRequest):

    result = engine.process(req.query)

    return {
        "status": "success",
        "input": req.query,
        "output": result
    }

# =========================================================
# STATUS
# =========================================================

@app.get("/status")
def status():

    return engine.status()

# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "timestamp": time.time()
    }

# =========================================================
# DEBUG LOGS
# =========================================================

@app.get("/logs")
def logs():

    try:
        return {
            "logs": engine.executor.logs[-100:]
        }

    except:
        return {
            "logs": []
        }