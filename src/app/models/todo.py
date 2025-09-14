from enum import IntEnum
from typing import Optional
from pydantic import BaseModel, Field


class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1


class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=200,
                           description='Name of the todo')
    todo_description: str = Field(..., min_length=3, max_length=200,
                                  description='Description of the todo')
    priority: Priority = Field(
        default=Priority.LOW, description='Priority of todo')


class TodoCreate(TodoBase):
    """Schema for creating a new todo"""
    pass


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo"""
    todo_name: Optional[str] = Field(
        None, min_length=3, max_length=200, description='Name of the todo')
    todo_description: Optional[str] = Field(
        None, min_length=3, max_length=200, description='Description of the todo')
    priority: Optional[Priority] = Field(
        None, description='Priority of todo')


class Todo(TodoBase):
    """Complete todo schema with ID"""
    todo_id: int = Field(..., description='Todo ID')

    class Config:
        # This allows Pydantic to work with ORM objects
        from_attributes = True