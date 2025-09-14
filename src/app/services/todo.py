from typing import List, Optional
from src.app.models.todo import Todo, TodoCreate, TodoUpdate, Priority


class TodoService:
    def __init__(self):
        # In-memory storage (in production, this would be a database)
        self.todos: List[Todo] = [
            Todo(todo_id=1, todo_name='sports',
                 todo_description='badminton game', priority=Priority.MEDIUM),
            Todo(todo_id=2, todo_name='work',
                 todo_description='complete project proposal', priority=Priority.HIGH),
            Todo(todo_id=3, todo_name='health',
                 todo_description='morning yoga session', priority=Priority.MEDIUM),
            Todo(todo_id=4, todo_name='learning',
                 todo_description='read 30 pages of JavaScript book', priority=Priority.LOW),
            Todo(todo_id=5, todo_name='personal',
                 todo_description='call mom for weekend plans', priority=Priority.LOW),
            Todo(todo_id=6, todo_name='finance',
                 todo_description='review monthly budget', priority=Priority.HIGH),
            Todo(todo_id=7, todo_name='home',
                 todo_description='organize desk workspace', priority=Priority.LOW),
            Todo(todo_id=8, todo_name='social',
                 todo_description='dinner with college friends', priority=Priority.LOW),
            Todo(todo_id=9, todo_name='hobby',
                 todo_description='practice guitar chords', priority=Priority.LOW),
            Todo(todo_id=10, todo_name='shopping',
                 todo_description='buy groceries for the week', priority=Priority.MEDIUM)
        ]

    def get_all_todos(self, limit: Optional[int] = None) -> List[Todo]:
        """Get all todos with optional limit"""
        if limit:
            return self.todos[:limit]
        return self.todos

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """Get a specific todo by ID"""
        for todo in self.todos:
            if todo.todo_id == todo_id:
                return todo
        return None

    def create_todo(self, todo_data: TodoCreate) -> Todo:
        """Create a new todo"""
        new_todo_id = max(t.todo_id for t in self.todos) + 1 if self.todos else 1
        
        new_todo = Todo(
            todo_id=new_todo_id,
            todo_name=todo_data.todo_name,
            todo_description=todo_data.todo_description,
            priority=todo_data.priority
        )
        
        self.todos.append(new_todo)
        return new_todo

    def update_todo(self, todo_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
        """Update an existing todo"""
        for index, todo in enumerate(self.todos):
            if todo.todo_id == todo_id:
                # Create update data dict, excluding unset values
                update_data = todo_update.dict(exclude_unset=True)
                
                # Update the todo with new data
                updated_todo = todo.copy(update=update_data)
                self.todos[index] = updated_todo
                return updated_todo
        return None

    def delete_todo(self, todo_id: int) -> Optional[Todo]:
        """Delete a todo by ID"""
        for index, todo in enumerate(self.todos):
            if todo.todo_id == todo_id:
                return self.todos.pop(index)
        return None


# Create a singleton instance
todo_service = TodoService()