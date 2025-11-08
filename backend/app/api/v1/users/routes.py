# app/api/users/routes.py

from fastapi import APIRouter, Depends
from app.api.v1.auth.dependencies import get_current_user

router = APIRouter(tags=["Users"])

@router.get("/me")
def read_users_me(user: dict = Depends(get_current_user)):
    """
    Returns the current user's data (decoded from JWT).
    """
    return {
        "id": user.get("sub"),
        "email": user.get("email"),
        "role": user.get("role"),
        "aud": user.get("aud"),
    }
