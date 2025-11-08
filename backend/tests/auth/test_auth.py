import pytest
import httpx
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings


SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY
AUDIENCE = "authenticated"

# Fixtures
@pytest.fixture
def supabase_test_user():
    import httpx

    email = "test_user@local.com"
    password = "password123"

    # 1️⃣ Sign up the user (returns access_token directly)
    signup_resp = httpx.post(
        f"{SUPABASE_URL}/auth/v1/signup",
        json={"email": email, "password": password},
        headers={"apikey": SUPABASE_KEY}
    )
    signup_resp.raise_for_status()
    access_token = signup_resp.json()["access_token"]
    user_id = signup_resp.json()["user"]["id"]

    yield access_token

    # 2️⃣ Cleanup
    httpx.delete(
        f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    )
@pytest.fixture
def expired_token():
    payload = {
        "sub": "fake-user-id",
        "email": "expired@local.com",
        "role": "admin",
        "aud": AUDIENCE,
        "exp": datetime.utcnow() - timedelta(minutes=10)  # already expired
    }
    return jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")

@pytest.fixture
def invalid_token():
    return "this.is.not.a.valid.jwt"

# Tests
def test_get_current_user(client, supabase_test_user):
    headers = {"Authorization": f"Bearer {supabase_test_user}"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_user@local.com"

def test_get_current_user_expired(client, expired_token):
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401  # Unauthorized

def test_get_current_user_invalid(client, invalid_token):
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401  # Unauthorized
