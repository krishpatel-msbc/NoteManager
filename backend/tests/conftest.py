import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.db.database import Base, get_db
from backend.main import app
from dotenv import load_dotenv
import os

# Load test env vars
load_dotenv(".env.test")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def clear_tables(db_session):
    # Truncate tables between tests
    db_session.execute(text("TRUNCATE TABLE note_tag_association RESTART IDENTITY CASCADE"))
    db_session.execute(text("TRUNCATE TABLE notes RESTART IDENTITY CASCADE"))
    db_session.execute(text("TRUNCATE TABLE tags RESTART IDENTITY CASCADE"))
    db_session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    db_session.commit()

@pytest.fixture
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = _override_get_db
    print("Registered routes:", [route.path for route in app.routes])
    with TestClient(app) as c:
        yield c

@pytest.fixture
def auth_header(client):
    user_res = client.post("/users/", json={"username": "testuser", "email": "testuser@example.com", "password": "securepass"})
    print("USER CREATE RESPONSE", user_res.status_code, user_res.text)
    assert user_res.status_code in (200, 201)
    login_res = client.post("/login", data={"username": "testuser@example.com", "password": "securepass"})
    print("LOGIN RESPONSE", login_res.status_code, login_res.text)
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}