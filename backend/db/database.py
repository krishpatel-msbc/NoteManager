import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from backend.core.config import settings

# Explicitly use test DB if TEST_MODE is set
#database_url = settings.DATABASE_URL
#if os.getenv("TEST_MODE") == "1":
#    database_url = settings.TEST_DATABASE_URL

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print(f"[DB Init] Using DB: {settings.DATABASE_URL}")