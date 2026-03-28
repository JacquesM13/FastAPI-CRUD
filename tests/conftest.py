import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app import models
from app.core.auth import create_access_token
from app.core.security import hash_password

# 1. Temporary SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Override get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3. Fixture for test client
@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)  # Create tables
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)    # Clean up

# 4. Fixture for test user
@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    user = models.User(email="test@email.com", hashed_password=hash_password("password"))
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

# 5. Fixture for auth headers
@pytest.fixture
def auth_headers(test_user):
    token = create_access_token({"user_id": test_user.id})
    return {"Authorization": f"Bearer {token}"}