# database/__init__.py
"""
Database package for Intelligent Career Path Planning System.
Provides SQLAlchemy connection management and normalized relational ORM models.
"""
from database.connection import get_db, init_db, engine, SessionLocal
from database.models import Base

__all__ = ["get_db", "init_db", "engine", "SessionLocal", "Base"]
