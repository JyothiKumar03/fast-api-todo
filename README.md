# FastAPI Todo Application

A well-structured FastAPI application for managing todos with proper Python project organization.

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   └── todo.py
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   └── todos.py
│   └── services/            # Business logic
│       ├── __init__.py
│       └── todo_service.py
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── run.py                  # Application runner
└── README.md
```

## Setup Instructions

### 1. Create Virtual Environment (Recommended)
```bash
# Create virtual environment using uv
uv venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
# Using uv (recommended - faster)
uv pip install -r requirements.txt

# Or using regular pip
pip install -r requirements.txt
```

### 3. Run the Application

**Option 1: Using run.py**
```bash
python run.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Option 3: Using FastAPI CLI (if installed)**
```bash
fastapi dev app/main.py
```

## API Endpoints

The API will be available at `http://localhost:8000`

### Base URL
- Root: `GET /` - Returns welcome message
- API Base: `/api/v1/todos`

### Todo Endpoints
- `GET /api/v1/todos/` - Get all todos (optional `limit` query parameter)
- `GET /api/v1/todos/{todo_id}` - Get specific todo by ID
- `POST /api/v1/todos/` - Create new todo
- `PUT /api/v1/todos/{todo_id}` - Update existing todo
- `DELETE /api/v1/todos/{todo_id}` - Delete todo by ID

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

### Create a Todo
```bash
curl -X POST "http://localhost:8000/api/v1/todos/" \
     -H "Content-Type: application/json" \
     -d '{
       "todo_name": "Learn Python",
       "todo_description": "Complete FastAPI tutorial",
       "priority": 2
     }'
```

### Get All Todos
```bash
curl "http://localhost:8000/api/v1/todos/"
```

### Update a Todo
```bash
curl -X PUT "http://localhost:8000/api/v1/todos/1" \
     -H "Content-Type: application/json" \
     -d '{
       "todo_name": "Updated Task",
       "priority": 1
     }'
```

## Key Features

- **Structured Architecture**: Proper separation of concerns
- **Pydantic Models**: Strong typing and validation
- **Service Layer**: Business logic separation
- **Router Organization**: Clean API endpoint organization
- **Error Handling**: Proper HTTP exception handling
- **Interactive Docs**: Auto-generated API documentation

## Priority Levels
- `1` = HIGH
- `2` = MEDIUM  
- `3` = LOW (default)