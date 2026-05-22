import os


class Config:

    # API SETTINGS
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

    # SECURITY
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # PERFORMANCE
    CACHE_TTL = int(os.getenv("CACHE_TTL", 300))

    # ENV MODE
    ENV = os.getenv("ENV", "development")