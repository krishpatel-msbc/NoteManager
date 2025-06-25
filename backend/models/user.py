"""
Defines the User ORM model for managing user accounts.
Each user can own multiple notes.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from backend.models.base import Base  
from backend.models.note import Note  

class User(Base):
    """
    SQLAlchemy model representing a user.

    Attributes:
        id: Unique identifier for the user.
        username: Unique username.
        email: Unique email address.
        hashed_password: Encrypted password.
        created_at: Timestamp of account creation.
        notes: One-to-many relationship to Note model.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    notes = relationship("Note", back_populates="owner")
