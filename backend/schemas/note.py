"""
Pydantic schemas for note and tag operations.

Defines serialization for creating, updating, and retrieving notes and their tags.
"""

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timezone



class TagBase(BaseModel):
    """
    Base schema for a tag (shared attributes).
    """
    name: str # Name of the tag

class TagCreate(TagBase):
    """
    Schema for creating a new tag.
    """
    pass

class Tag(TagBase):
    """
    Schema returned when reading a tag from the database.
    """
    id: int

    class Config:
        orm_mode = True # Enables ORM compatibility


class NoteBase(BaseModel):
    """
    Base schema for a note (shared attributes).
    """
    title: str
    content: Optional[str] = None # Optional note content

class NoteCreate(NoteBase):
    """
    Schema for creating a new note with optional tags.
    """
    tags: Optional[List[TagCreate]] = []

class NoteUpdate(NoteBase):
    """
    Schema for updating an existing note.
    Tags can also be updated.
    """
    tags: Optional[List[TagCreate]] = []

class NoteInDBBase(NoteBase):
    """
    Base schema for a note retrieved from the database.
    Includes system-generated fields.
    """
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[Tag] = [] # List of associated Tags

    class Config:
        orm_mode = True # Enables ORM compatibility

class Note(NoteInDBBase):
    """
    Schema returned in API responses.
    Inherits all fields from NoteInDBBase.
    """
    pass


