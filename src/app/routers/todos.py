from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from src.app.models.todo import Todo, TodoCreate, TodoUpdate
from src.app.services.todo import todo_service

# Create router instance
router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Todo])
def get_todos(limit: Optional[int] = Query(None, description="Limit the number of todos returned")):
    """Get all todos with optional limit"""
    return todo_service.get_all_todos(limit=limit)


@router.get("/{todo_id}", response_model=Todo)
def get_todo_by_id(todo_id: int):
    """Get a specific todo by ID"""
    print(f'todo_id received: {todo_id}')

    todo = todo_service.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.post("/", response_model=Todo)
def create_todo(todo: TodoCreate):
    """Create a new todo"""
    new_todo = todo_service.create_todo(todo)
    print(f'Created new todo with id: {new_todo.todo_id}')
    return new_todo


@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    """Update an existing todo"""
    todo = todo_service.update_todo(todo_id, updated_todo)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.delete("/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int):
    """Delete a todo by ID"""
    deleted_todo = todo_service.delete_todo(todo_id)
    if not deleted_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return deleted_todo
