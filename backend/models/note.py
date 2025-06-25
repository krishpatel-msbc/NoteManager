"""
Defines the Note and Tag ORM models and their many-to-many relationship.

Note: Represents a user-created note with tags.
Tag: Represents a label that can be attached to multiple notes.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from backend.models.base import Base


# Association table for many-to-many relationship between notes and tags
note_tag_association = Table(
    "note_tag_association",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Note(Base):
    """
    SQLAlchemy model representing a note.

    Attributes:
        id: Unique identifier for the note.
        title: Short title of the note.
        content: Full content/text of the note.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last update.
        owner_id: Foreign key linking to the note's creator (User).
        owner: Relationship to the User model.
        tags: Many-to-many relationship with Tag model.
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="notes")

    tags = relationship("Tag", secondary=note_tag_association, back_populates="notes")


class Tag(Base):
    """
    SQLAlchemy model representing a Tag.
    Attributes:
        id: Unique identifier.
        name: Tag name (unique).
        notes: Many-to-many relationship with Note model.
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    notes = relationship("Note", secondary=note_tag_association, back_populates="tags")
