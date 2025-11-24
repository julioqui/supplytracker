from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.middleware.auth import AuthMiddleware  # <-- import your middleware

app = FastAPI(title="SupplyTracker API")

# CORS
origins = [
    "http://127.0.0.1:3000",  # frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # permite Authorization header
    allow_methods=["*"],     # GET, POST, OPTIONS, etc
    allow_headers=["*"],     # Authorization, Content-Type, etc
)

# Add auth middleware
app.add_middleware(AuthMiddleware)

# API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def healthcheck():
    return {"status": "ok"}
