from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.middleware.auth import AuthMiddleware
from app.core.config import settings 

app = FastAPI(title="SupplyTracker API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Add auth middleware
app.add_middleware(AuthMiddleware)

# API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def healthcheck():
    return {"status": "ok"}
