# database/connection.py
"""
Database connection management for Intelligent Career Path Planning System.
Supports SQLite out-of-the-box (zero configuration) and PostgreSQL in production.
"""
import os
from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine

# Default to local SQLite database in project root
DEFAULT_DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "career_intelligence.db"))
DATABASE_URL = os.environ.get("CAREER_DB_URL", f"sqlite:///{DEFAULT_DB_FILE}")

# Enforce foreign key constraints on SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

# Connection arguments
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Generator yielding a database session for request lifecycles."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_session():
    """Context manager for safe transactional database sessions."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """Creates all database tables defined in models.py."""
    from database.models import Base
    Base.metadata.create_all(bind=engine)
    return engine
