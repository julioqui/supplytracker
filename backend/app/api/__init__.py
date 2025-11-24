from fastapi import APIRouter
from app.api.v1.supplies import routes as supplies_routes
from app.api.v1.users import routes as users_routes
from app.api.v1.auth import routes as auth_routes

api_router = APIRouter()
api_router.include_router(users_routes.router)
api_router.include_router(supplies_routes.router)
api_router.include_router(auth_routes.router)