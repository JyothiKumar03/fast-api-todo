# database/__init__.py - Database package initialization
"""Database package for FastAPI Todo application."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
load_dotenv()
DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or os.getenv("NEON_DB_URL")
    or "sqlite:///./todos.db"
)

# Create SQLAlchemy engine
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Import models after Base is defined to avoid circular imports
from .todo_model import TodoModel  # noqa: E402

# Database dependency for FastAPI


def get_db():
    """
    Database dependency that provides a database session.
    Used with FastAPI's dependency injection system.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all tables

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
