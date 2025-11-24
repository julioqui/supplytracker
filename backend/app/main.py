from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import api_router
from app.middleware.auth import AuthMiddleware
from app.core.config import settings 

app = FastAPI(title="SupplyTracker API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add auth middleware
app.add_middleware(AuthMiddleware)

# API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def healthcheck():
    return {"status": "ok"}
