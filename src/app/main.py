"""
FastAPI Todo Application Main Module.
Entry point for the Todo API with proper database initialization.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import routers
from .routers import todos
# Import database setup
from .database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup: Create database tables
    create_tables()
    yield
    # Shutdown: Clean up resources if needed


# Create FastAPI instance with lifespan management
app = FastAPI(
    title="Todo API",
    description="A simple Todo API built with FastAPI and SQLAlchemy",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers with proper prefix
app.include_router(todos.router, prefix="/api/v1")


# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint returning a welcome message"""
    return {"message": "Hello Python! Welcome to the Todo API"}
