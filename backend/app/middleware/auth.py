from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.v1.auth.dependencies import get_current_user

EXCLUDE_PATHS = ["/auth", "/auth/", "/docs", "/openapi.json", "/public"]  # add any routes that don't need auth

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip paths that don't require auth
        for path in EXCLUDE_PATHS:
            if request.url.path.startswith(path):
                return await call_next(request)

        # Check token using your existing get_current_user
        try:
            await get_current_user(request)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

        response = await call_next(request)
        return response
