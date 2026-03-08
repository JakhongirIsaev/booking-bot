"""
SQLAlchemy declarative base for all models.

All models inherit from this Base class.
Import Base where you define models, import metadata for Alembic.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass
