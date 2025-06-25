"""
Database configuration module.

This sets up the SQLAlchemy engine, session factory, and base class for models.
It also provides the `get_db` dependency for creating and closing database sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from backend.core.config import settings


# Create the SQLAlchemy engine using the database URL from settings
engine = create_engine(settings.DATABASE_URL)


# Session factory for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for all SQLAlchemy models
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.

    Yields:
        SQLAlchemy Session: a database session to be used in API routes or services.
    
    Ensures the session is properly closed after use.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        