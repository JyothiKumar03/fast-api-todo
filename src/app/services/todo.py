# services/todo.py - Service Layer for Todo Operations
"""
Service layer that bridges Pydantic schemas and SQLAlchemy models.
Handles business logic and database operations for todos.

Flow: API Request (Pydantic) → Database (SQLAlchemy) → API Response (Pydantic)
"""

from typing import List, Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import or_

# Import database components
from ..database import SessionLocal, get_db
from ..database.todo_model import TodoModel
# Import Pydantic models for validation and serialization
from ..models.todo import Todo, TodoCreate, TodoUpdate, Priority


class TodoService:
    """
    Service layer that bridges Pydantic schemas and SQLAlchemy models

    Flow: API Request (Pydantic) → Database (SQLAlchemy) → API Response (Pydantic)
    """

    @staticmethod
    def get_all_todos(limit: Optional[int] = None) -> List[Todo]:
        """Get all todos as Pydantic models with optional limit"""
        db = SessionLocal()
        try:
            query = db.query(TodoModel).order_by(
                TodoModel.priority.asc(),
                TodoModel.created_at.desc()
            )

            if limit:
                query = query.limit(limit)

            todo_models = query.all()
            print('todo_models',todo_models)

            # Convert SQLAlchemy models to Pydantic models
            return [todo_model.to_pydantic() for todo_model in todo_models]

        except SQLAlchemyError as e:
            raise Exception(f"Database error retrieving todos: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def get_todo_by_id(todo_id: int) -> Optional[Todo]:
        """Get a specific todo by ID as Pydantic model"""
        db = SessionLocal()
        try:
            todo_model = db.query(TodoModel).filter(
                TodoModel.todo_id == todo_id).first()
            return todo_model.to_pydantic() if todo_model else None

        except SQLAlchemyError as e:
            raise Exception(
                f"Database error retrieving todo {todo_id}: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def create_todo(todo_create: TodoCreate) -> Todo:
        """
        Create a new todo from Pydantic TodoCreate model
        Returns Pydantic Todo model
        """
        db = SessionLocal()
        try:
            # Convert Pydantic → SQLAlchemy
            todo_model = TodoModel.from_pydantic_create(todo_create)

            # Save to database
            db.add(todo_model)
            db.commit()
            db.refresh(todo_model)  # Get the generated ID

            # Return as Pydantic model
            return todo_model.to_pydantic()

        except IntegrityError as e:
            db.rollback()
            raise ValueError(f"Invalid data: {str(e)}")
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Database error creating todo: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def update_todo(todo_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
        """
        Update an existing todo with Pydantic TodoUpdate model
        Returns updated Pydantic Todo model
        """
        db = SessionLocal()
        try:
            todo_model = db.query(TodoModel).filter(
                TodoModel.todo_id == todo_id).first()
            if not todo_model:
                return None

            # Update using Pydantic model
            todo_model.update_from_pydantic(todo_update)

            # Save changes
            db.commit()
            db.refresh(todo_model)

            # Return as Pydantic model
            return todo_model.to_pydantic()

        except IntegrityError as e:
            db.rollback()
            raise ValueError(f"Invalid update data: {str(e)}")
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(
                f"Database error updating todo {todo_id}: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def delete_todo(todo_id: int) -> Optional[Todo]:
        """Delete a todo by ID and return the deleted todo"""
        db = SessionLocal()
        try:
            todo_model = db.query(TodoModel).filter(
                TodoModel.todo_id == todo_id).first()
            if not todo_model:
                return None

            # Get the todo data before deletion
            deleted_todo = todo_model.to_pydantic()

            db.delete(todo_model)
            db.commit()

            return deleted_todo

        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(
                f"Database error deleting todo {todo_id}: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def get_todos_by_priority(priority: Priority) -> List[Todo]:
        """Get todos filtered by priority enum"""
        db = SessionLocal()
        try:
            todo_models = db.query(TodoModel).filter(
                TodoModel.priority == priority.value
            ).order_by(TodoModel.created_at.desc()).all()

            return [todo_model.to_pydantic() for todo_model in todo_models]

        except SQLAlchemyError as e:
            raise Exception(f"Database error filtering todos: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def search_todos(search_term: str) -> List[Todo]:
        """Search todos by name or description"""
        db = SessionLocal()
        try:
            search_pattern = f"%{search_term}%"
            todo_models = db.query(TodoModel).filter(
                or_(
                    TodoModel.todo_name.ilike(search_pattern),
                    TodoModel.todo_description.ilike(search_pattern)
                )
            ).order_by(TodoModel.priority.asc(), TodoModel.created_at.desc()).all()

            return [todo_model.to_pydantic() for todo_model in todo_models]

        except SQLAlchemyError as e:
            raise Exception(f"Database error searching todos: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def seed_initial_data() -> dict:
        """Seed database with initial todo data using Pydantic models"""
        initial_todos_data = [
            {'todo_name': 'sports', 'todo_description': 'badminton game',
                'priority': Priority.LOW},
            {'todo_name': 'work', 'todo_description': 'complete project proposal',
                'priority': Priority.HIGH},
            {'todo_name': 'health', 'todo_description': 'morning yoga session',
                'priority': Priority.MEDIUM},
            {'todo_name': 'learning', 'todo_description': 'read 30 pages of JavaScript book',
                'priority': Priority.MEDIUM},
            {'todo_name': 'personal', 'todo_description': 'call mom for weekend plans',
                'priority': Priority.LOW},
            {'todo_name': 'finance', 'todo_description': 'review monthly budget',
                'priority': Priority.HIGH},
            {'todo_name': 'home', 'todo_description': 'organize desk workspace',
                'priority': Priority.LOW},
            {'todo_name': 'social', 'todo_description': 'dinner with college friends',
                'priority': Priority.LOW},
            {'todo_name': 'hobby', 'todo_description': 'practice guitar chords',
                'priority': Priority.LOW},
            {'todo_name': 'shopping', 'todo_description': 'buy groceries for the week',
                'priority': Priority.MEDIUM}
        ]

        db = SessionLocal()
        try:
            # Check if data already exists
            if db.query(TodoModel).count() > 0:
                return {"message": "Data already exists"}

            # Create todos using Pydantic validation
            for todo_data in initial_todos_data:
                todo_create = TodoCreate(**todo_data)  # Pydantic validation
                todo_model = TodoModel.from_pydantic_create(todo_create)
                db.add(todo_model)

            db.commit()
            return {"message": f"Seeded {len(initial_todos_data)} todos successfully"}

        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Database error seeding data: {str(e)}")
        finally:
            db.close()


# Create a service instance for use in routers
todo_service = TodoService()
