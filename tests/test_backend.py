import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from database import get_db

DATABASE_URL = "postgresql://user:password@localhost/test_db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def create_user(db_session):
    user = User(username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_create_user(test_client, db_session):
    response = test_client.post("/users/", json={"username": "newuser", "email": "new@example.com"})
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"

def test_get_user(test_client, create_user):
    response = test_client.get(f"/users/{create_user.id}")
    assert response.status_code == 200
    assert response.json()["username"] == create_user.username

def test_update_user(test_client, create_user):
    response = test_client.put(f"/users/{create_user.id}", json={"username": "updateduser"})
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"

def test_delete_user(test_client, create_user):
    response = test_client.delete(f"/users/{create_user.id}")
    assert response.status_code == 204
    response = test_client.get(f"/users/{create_user.id}")
    assert response.status_code == 404

def test_invalid_user_creation(test_client):
    response = test_client.post("/users/", json={"username": "", "email": "invalid"})
    assert response.status_code == 422
    assert "value is not a valid string" in response.json()["detail"][0]["msg"]

def test_database_connection():
    try:
        db = TestingSessionLocal()
        assert db is not None
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")