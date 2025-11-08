from app.core.config import settings
import requests
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_JWT_SECRET = settings.SUPABASE_JWT_SECRET  # HS256 secret
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

    # Attempt HS256
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.JWTError as e:
        print("HS256 JWT decode error:", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(token: str = Depends(security)):
    return verify_supabase_jwt(token.credentials)
