"""
Pydantic schemas for user-related operations.

Includes schemas for user creation, update, reading from the DB, and API responses.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """
    Shared base schema for user data used in reading and writing.
    """
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str # Raw password to be hashed


class UserUpdate(BaseModel):
    """
    Schema for updating user details.
    All fields are optional.
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    """
    Base schema used when reading a user from the database.
    Includes DB-only fields.
    """
    id: int
    created_at: datetime

    class Config:
        orm_mode = True # Enables ORM compatibility


class User(UserInDBBase):
    """
    Schema returned in API responses.
    Inherits all fields from UserInDBBase.
    """
    pass


