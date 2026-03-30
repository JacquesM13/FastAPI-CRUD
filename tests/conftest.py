import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app import models
from app.core.auth import create_access_token
from app.core.security import hash_password
from sqlalchemy.pool import StaticPool
import uuid

# Temporary SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    user = models.User(
        email=f"test_{uuid.uuid4()}@mail.com",
        hashed_password=hash_password("password")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user_task(db, test_user):
    task = models.Task(
        title="My task",
        user_id=test_user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@pytest.fixture
def other_user(db):
    user = models.User(
        email=f"other_{uuid.uuid4()}@mail.com",
        hashed_password=hash_password("other")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def other_user_task(db, other_user):
    task = models.Task(
        title="Other user's task",
        user_id=other_user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@pytest.fixture
def auth_headers_for_user():
    def _auth(user):
        token = create_access_token({"user_id": user.id})
        return {"Authorization": f"Bearer {token}"}
    return _auth