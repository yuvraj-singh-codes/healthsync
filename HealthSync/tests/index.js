import pytest
from fastapi.testclient import TestClient
from HealthSync.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from HealthSync.database import get_db, Base
from HealthSync.models import User, Item

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    yield db
    db.close()

def test_create_user(test_client, db_session):
    response = test_client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_read_user(test_client, db_session):
    response = test_client.get("/users/testuser")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_create_item(test_client, db_session):
    response = test_client.post("/items/", json={"name": "testitem", "owner": "testuser"})
    assert response.status_code == 201
    assert response.json()["name"] == "testitem"

def test_read_item(test_client, db_session):
    response = test_client.get("/items/testitem")
    assert response.status_code == 200
    assert response.json()["name"] == "testitem"

def test_integration(test_client, db_session):
    user_response = test_client.post("/users/", json={"username": "integrationuser", "email": "integration@example.com"})
    item_response = test_client.post("/items/", json={"name": "integrationitem", "owner": "integrationuser"})
    
    assert user_response.status_code == 201
    assert item_response.status_code == 201

    user_check = test_client.get("/users/integrationuser")
    item_check = test_client.get("/items/integrationitem")
    
    assert user_check.status_code == 200
    assert item_check.status_code == 200

def test_error_handling(test_client):
    response = test_client.get("/users/nonexistentuser")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_invalid_data(test_client):
    response = test_client.post("/users/", json={"username": "", "email": "invalidemail"})
    assert response.status_code == 422
    assert "value is not a valid string" in response.json()["detail"][0]["msg"]