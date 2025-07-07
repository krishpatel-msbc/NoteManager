"""
Defines the base class for all SQLAlchemy ORM models.
Used to create database tables via declarative mapping.
"""

from sqlalchemy.orm import declarative_base

# Base class for all ORM models
Base = declarative_base()
