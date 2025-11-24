from app.core.config import settings
import requests
from jose import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer

# Validate environment
if not hasattr(settings, 'APP_ENV') or settings.APP_ENV not in ["development", "production", "staging"]:
    raise ValueError(
        "Invalid or missing APP_ENV value. "
        "Must be one of: development, production, staging. "
        f"Current value: {getattr(settings, 'APP_ENV', 'not set')}"
    )

security = HTTPBearer()

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_JWT_SECRET = settings.SUPABASE_JWT_SECRET
SUPABASE_JWKS_URL = f"{SUPABASE_URL}/auth/v1/keys"

_jwks_cache = None

def get_supabase_public_keys():
    global _jwks_cache
    if _jwks_cache is None:
        res = requests.get(SUPABASE_JWKS_URL)
        if not res.ok:
            raise HTTPException(status_code=500, detail="Failed to fetch Supabase JWKS")
        _jwks_cache = res.json().get("keys", [])
    return _jwks_cache

def verify_supabase_jwt(token: str):
    # Attempt RS256
    try:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        if kid:
            keys = get_supabase_public_keys()
            key = next((k for k in keys if k["kid"] == kid), None)
            if key:
                payload = jwt.decode(token, key, algorithms=["RS256"], audience="authenticated")
                return payload
    except Exception as e:
        print("RS256 verification failed:", e)

    # Attempt HS256 for local development testing
    if settings.APP_ENV == "development":
        try:
            payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except jwt.JWTError as e:
            print("HS256 JWT decode error:", e)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token")

    token = auth_header.split(" ")[1]

    try:
        # First try to verify with RS256 (Supabase public key)
        try:
            return verify_supabase_jwt(token)
        except HTTPException as e:
            if e.detail != "Invalid token":
                raise
            
        # Attempt HS256 for local development testing
        if settings.APP_ENV == "development":
            payload = jwt.decode(
                token, 
                settings.SUPABASE_JWT_SECRET, 
                algorithms=["HS256"],
            )
            return payload
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError as e:
        print(f"JWT validation error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")