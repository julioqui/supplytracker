from fastapi import APIRouter, Depends
from app.api.v1.auth.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])
