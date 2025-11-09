from fastapi import FastAPI
from app.api.v1.users.routes import router as users_router
from fastapi.middleware.cors import CORSMiddleware

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

# Routes
app.include_router(users_router, prefix="/api/v1/users")

@app.get("/health")
def healthcheck():
    return {"status": "ok"}
