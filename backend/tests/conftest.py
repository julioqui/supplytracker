import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base
from app.main import app

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
def db_session(test_db_engine):
    Session = sessionmaker(bind=test_db_engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()

# -------------------------------
# FastAPI TestClient
# -------------------------------
@pytest.fixture(scope="function")
def client():
    return TestClient(app)
