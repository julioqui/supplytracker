import os
import pytest
from app.core.db import Base, engine, SessionLocal
from app.core.config import settings

# Define test environment
@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    os.environ["ENV_FILE"] = ".env.test"
    os.environ["APP_ENV"] = "test"

    from app.core.config import settings

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)

# Fixture that provides a DB session for each test
@pytest.fixture()
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
