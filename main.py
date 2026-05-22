from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.chat_routes import router as chat_router
from dashboard.routes import router as dashboard_router
from api.webhooks.billing_webhook import router as billing_webhook_router

app = FastAPI(title="Matrix X")

app.include_router(chat_router)
app.include_router(dashboard_router, prefix="/dashboard")
app.include_router(billing_webhook_router)

app.mount("/ui", StaticFiles(directory="dashboard_ui", html=True), name="ui")


@app.get("/")
def home():
    return {"status": "online", "ui": "/ui"}