# database/todo_model.py - SQLAlchemy Database Model
"""
SQLAlchemy model for the todos table.
Works with Pydantic schemas for data validation and serialization.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from . import Base
# Import Pydantic models for type conversion
from ..models.todo import Priority, Todo, TodoCreate, TodoUpdate


class TodoModel(Base):
    """
    SQLAlchemy model for todos table
    Works with your existing Pydantic schemas in /app/models/todo.py
    """
    __tablename__ = 'todos'

    # Primary key
    todo_id = Column(Integer, primary_key=True, index=True)

    # Fields matching your Pydantic schema exactly
    todo_name = Column(
        String(200),
        nullable=False,
        index=True  # For search performance
    )

    todo_description = Column(
        String(200),
        nullable=False
    )

    # Priority using your existing Priority enum
    priority = Column(
        Integer,
        default=Priority.LOW.value,
        nullable=False,
        index=True  # For filtering by priority
    )

    # Timestamps (database managed)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Database constraints (matches your Pydantic validation)
    __table_args__ = (
        CheckConstraint('length(todo_name) >= 3',
                        name='check_todo_name_length'),
        CheckConstraint('length(todo_description) >= 3',
                        name='check_todo_description_length'),
        CheckConstraint('priority IN (1, 2, 3)', name='check_priority_values'),
    )

    def __repr__(self):
        return f'<TodoModel {self.todo_id}: {self.todo_name}>'

    def to_pydantic(self):
        """
        Convert SQLAlchemy model to Pydantic Todo model
        This bridges database → API response
        """

        return Todo(
            todo_id=self.todo_id,
            todo_name=self.todo_name,
            todo_description=self.todo_description,
            priority=Priority(self.priority)
        )

    def to_dict(self):
        """Convert to dictionary (for JSON responses)"""
        return {
            'todo_id': self.todo_id,
            'todo_name': self.todo_name,
            'todo_description': self.todo_description,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_pydantic_create(cls, pydantic_todo):
        """
        Create SQLAlchemy model from Pydantic TodoCreate
        This bridges API request → database
        """
        return cls(
            todo_name=pydantic_todo.todo_name,
            todo_description=pydantic_todo.todo_description,
            priority=pydantic_todo.priority.value  # Convert enum to int
        )

    def update_from_pydantic(self, pydantic_update):
        """
        Update SQLAlchemy model from Pydantic TodoUpdate
        Only updates non-None fields
        """
        if pydantic_update.todo_name is not None:
            self.todo_name = pydantic_update.todo_name

        if pydantic_update.todo_description is not None:
            self.todo_description = pydantic_update.todo_description

        if pydantic_update.priority is not None:
            self.priority = pydantic_update.priority.value
