from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.v1.auth.dependencies import get_current_user

EXCLUDE_PATHS = ["/auth", "/auth/", "/docs", "/openapi.json", "/public"]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip OPTIONS requests
        if request.method == "OPTIONS":
            return await call_next(request)
            
        # Skip paths that don't require auth
        if any(request.url.path.startswith(path) for path in EXCLUDE_PATHS):
            return await call_next(request)

        # Check token
        try:
            await get_current_user(request)
            return await call_next(request)
        except HTTPException as e:
            if e.status_code == status.HTTP_401_UNAUTHORIZED:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": e.detail}
                )
            raise e