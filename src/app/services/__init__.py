"""
Services package for business logic.
Contains service classes that handle operations between API and database layers.
"""

from .todo import TodoService, todo_service

# Re-export the service class and configured singleton for package-level imports
__all__ = ["TodoService", "todo_service"]
