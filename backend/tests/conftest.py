import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base, engine, SessionLocal as BaseSessionLocal
from app.main import app
from app.db.models import User, Tenant
from app.db.session import get_db
import jwt
import time
import uuid
from datetime import datetime

# Override the database URL for tests
settings.DB_URL = settings.TEST_DB_URL

# Create a new session factory for tests
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the test database
Base.metadata.create_all(bind=engine)

# -------------------------------
# Test DB setup
# -------------------------------
@pytest.fixture(scope="session")
def test_db_engine():
    engine = create_engine(settings.TEST_DB_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Clean up all data after each test
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()

# -------------------------------
# FastAPI TestClient
# -------------------------------
@pytest.fixture(scope="function")
def client(db_session):
    # Override the get_db dependency to use the test database session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Don't close the session here, it's managed by the fixture
    
    # Apply the override
    app.dependency_overrides[get_db] = override_get_db
    
    # Create and return the test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear the overrides after the test
    app.dependency_overrides.clear()

# -------------------------------
# Tenant fixtures
# -------------------------------
@pytest.fixture
def test_tenant(db_session):
    """Create a test tenant."""
    tenant = Tenant(
        id=uuid.uuid4(),
        name=f"Test Tenant {uuid.uuid4().hex[:8]}",
        domain=f"test-{uuid.uuid4().hex[:8]}.example.com"
    )
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)
    return tenant

# -------------------------------
# Auth fixtures
# -------------------------------
@pytest.fixture
def supabase_test_user(db_session, test_tenant, request):
    # Create a unique email for each test run
    unique_email = f"test_user_{uuid.uuid4().hex[:8]}@local.com"
    
    # Create a test user associated with the test tenant
    user = User(
        id=str(uuid.uuid4()),
        email=unique_email,
        tenant_id=test_tenant.id
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Register cleanup using the request fixture
    request.addfinalizer(
        lambda: db_session.query(User).filter(User.id == user.id).delete() or db_session.commit()
    )
    
    payload = {
        "sub": user.id,
        "email": user.email,
        "app_metadata": {},
        "user_metadata": {},
        "role": "authenticated",
        "exp": int(time.time()) + 3600
    }
    
    token = jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")
    return {"user": user, "token": token}

@pytest.fixture
def valid_token(db_session, test_tenant, request):
    # Create a unique email for each test run
    unique_email = f"valid_user_{uuid.uuid4().hex[:8]}@local.com"
    
    # Create a test user associated with the test tenant
    user = User(
        id=str(uuid.uuid4()),
        email=unique_email,
        tenant_id=test_tenant.id,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db_session.add(user)
    db_session.commit()
    
    payload = {
        "sub": user.id,
        "email": user.email,
        "role": "authenticated",
        "exp": int(time.time()) + 3600,
    }
    
    token = jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")
    
    # Register cleanup using the request fixture
    request.addfinalizer(
        lambda: db_session.query(User).filter(User.id == user.id).delete() or db_session.commit()
    )
    
    return token
