import pytest
import time
import uuid
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings
from app.db.models import User, Tenant
from fastapi import HTTPException

AUDIENCE = "authenticated"

# -------------------------------
# Tenant fixture
# -------------------------------
@pytest.fixture
def test_tenant(db_session):
    """Create a test tenant."""
    tenant = Tenant(
        id=str(uuid.uuid4()),
        name=f"Test Tenant {uuid.uuid4().hex[:6]}",
        domain=f"tenant-{uuid.uuid4().hex[:6]}.example.com"
    )
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)
    return tenant

# -------------------------------
# User fixture
# -------------------------------
@pytest.fixture
def supabase_test_user(db_session, test_tenant):
    """Create a test user and JWT."""
    user = User(
        id=str(uuid.uuid4()),
        email=f"test_user_{uuid.uuid4().hex[:6]}@local.com",
        tenant_id=test_tenant.id,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    payload = {
        "sub": user.id,
        "email": user.email,
        "role": "authenticated",
        "aud": AUDIENCE,
        "exp": int(time.time()) + 3600  # expires in 1 hour
    }

    token = jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")

    return {"user": user, "token": token}

# -------------------------------
# Expired / invalid token fixtures
# -------------------------------
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

# -------------------------------
# Tests
# -------------------------------
def test_get_current_user(client, supabase_test_user):
    headers = {"Authorization": f"Bearer {supabase_test_user['token']}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == supabase_test_user["user"].email

from fastapi import HTTPException

def test_get_current_user_expired(client, expired_token):
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Token expired"

def test_get_current_user_invalid(client, invalid_token):
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"
