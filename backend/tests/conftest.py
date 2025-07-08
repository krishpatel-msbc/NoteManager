import os
from dotenv import load_dotenv
# Force load test .env before anything else
load_dotenv(".env.test", override=True)
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from alembic.config import Config
from alembic import command

from backend.db.database import get_db
from backend.main import app
from backend.core.config import settings

# Fail fast if not using test DB
if "test" not in settings.DATABASE_URL:
    raise RuntimeError(f"[ABORTED] Unsafe DATABASE_URL: {settings.DATABASE_URL}")

# Setup SQLAlchemy engine for the test database
engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_alembic_migrations():
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "../../alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    run_alembic_migrations()
    yield
    # Optional teardown: drop all tables
    # from backend.models.base import Base
    # Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def clear_tables(db_session):
    # Clear data between tests
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
    with TestClient(app) as c:
        yield c

@pytest.fixture
def auth_header(client):
    user_res = client.post("/users/", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepass"
    })
    assert user_res.status_code in (200, 201)

    login_res = client.post("/login", data={
        "username": "testuser@example.com",
        "password": "securepass"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
