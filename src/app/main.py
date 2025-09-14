from fastapi import FastAPI
from src.app.routers import todos

# Create FastAPI instance
app = FastAPI(
    title="Todo API",
    description="A simple Todo API built with FastAPI",
    version="1.0.0"
)

# Include routers
app.include_router(todos.router, prefix="/api/v1")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello Python!"}

# from fastapi import FastAPI
# from enum import IntEnum
# from typing import List, Optional
# from pydantic import BaseModel, Field
# from fastapi import HTTPException


# api = FastAPI()


# class Priority(IntEnum):
#     LOW = 3
#     MEDIUM = 2
#     HIGH = 1


# class TodoBase(BaseModel):
#     todo_name: str = Field(..., min_length=3, max_length=200,
#                            description='name of the todo')
#     todo_description: str = Field(..., min_length=3, max_length=200,
#                                   description='description of the todo')  # Fixed field name
#     priority: Priority = Field(
#         default=Priority.LOW, description='priority of todo')


# class TodoCreate(TodoBase):
#     pass


# class Todo(TodoBase):
#     todo_id: int = Field(..., description='Todo id')  # Fixed description


# class TodoUpdate(BaseModel):
#     todo_name: Optional[str] = Field(
#         None, min_length=3, max_length=200, description='name of the todo')
#     todo_description: Optional[str] = Field(
#         None, min_length=3, max_length=200, description='description of the todo')  # Fixed field name
#     priority: Optional[Priority] = Field(
#         None, description='priority of todo')  # Fixed: None instead of default


# all_todos = [
#     Todo(todo_id=1, todo_name='sports',
#          todo_description='badminton game', priority=Priority.MEDIUM),
#     Todo(todo_id=2, todo_name='work',
#          todo_description='complete project proposal', priority=Priority.HIGH),
#     Todo(todo_id=3, todo_name='health',
#          todo_description='morning yoga session', priority=Priority.MEDIUM),
#     Todo(todo_id=4, todo_name='learning',
#          todo_description='read 30 pages of JavaScript book', priority=Priority.LOW),
#     Todo(todo_id=5, todo_name='personal',
#          todo_description='call mom for weekend plans', priority=Priority.LOW),
#     Todo(todo_id=6, todo_name='finance',
#          todo_description='review monthly budget', priority=Priority.HIGH),
#     Todo(todo_id=7, todo_name='home',
#          todo_description='organize desk workspace', priority=Priority.LOW),
#     Todo(todo_id=8, todo_name='social',
#          todo_description='dinner with college friends', priority=Priority.LOW),
#     Todo(todo_id=9, todo_name='hobby',
#          todo_description='practice guitar chords', priority=Priority.LOW),
#     Todo(todo_id=10, todo_name='shopping',
#          todo_description='buy groceries for the week', priority=Priority.MEDIUM)
# ]


# @api.get('/')
# def index():
#     return {"message": "Hello Python!"}


# @api.get('/todos/{todo_id}', response_model=Todo)
# def get_todo_by_id(todo_id: int):
#     print('todo_id received: ', todo_id)
#     for todo in all_todos:
#         if todo.todo_id == todo_id:  # Fixed: dot notation
#             return todo  # Fixed: direct return
#     raise HTTPException(status_code=404, detail="Todo not found")


# @api.get('/todos', response_model=List[Todo])
# def get_todos(limit:int=None):
#     if limit:
#         return all_todos[:int(limit)]  # Fixed: direct return
#     return all_todos  # Fixed: direct return


# @api.post('/todos', response_model=Todo)
# def create_todos(todo: TodoCreate):
#     new_todo_id = max(t.todo_id for t in all_todos) + 1  # Fixed: dot notation
#     print('new_todo_id', new_todo_id)

#     # Fixed: create Todo object
#     new_todo = Todo(todo_id=new_todo_id, **todo.dict())
#     all_todos.append(new_todo)
#     return new_todo


# @api.put('/todos/{todo_id}', response_model=Todo)
# def update_todos(todo_id: int, updated_todo: TodoUpdate):
#     for index, todo in enumerate(all_todos):
#         if todo.todo_id == todo_id:
#             # Fixed: Create new object with updated fields
#             update_data = updated_todo.dict(exclude_unset=True)
#             updated_todo_obj = todo.copy(update=update_data)
#             all_todos[index] = updated_todo_obj
#             return updated_todo_obj
#     return None  # or raise HTTPException


# @api.delete('/todos/{todo_id}', response_model=Todo)
# def delete_todo(todo_id: int):
#     for index, todo in enumerate(all_todos):
#         if todo.todo_id == todo_id:  # Fixed: dot notation
#             deleted_todo = all_todos.pop(index)
#             return deleted_todo
#     return None  # or raise HTTPException
