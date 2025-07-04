"""
Main application entrypoint for the NoteManager API.
Initializes the FastAPI app, includes routes, and handles startup/shutdown logging.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from backend.db.database import engine
from backend.models.base import Base
from backend.models.user import User
from backend.models.note import Note, Tag
from backend.api.route_user import router as user_router
from backend.api.route_note import router as note_router
from backend.api.route_auth import router as auth_router 
from backend.logger import logger
from dotenv import load_dotenv
import os
from backend.utils.audit_watcher import audit_log_watcher
import threading


# Load environment variables from .env file
load_dotenv()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Logs messages when the app starts and shuts down.
    """
    logger.info("NoteManager API is starting up...")
    # start audit log watcher
    thread = threading.Thread(target = audit_log_watcher, daemon = True)
    thread.start()
    yield
    logger.info("NoteManager API is shutting down...")

# Initialize FastAPI app with metadata and lifespan handler
app = FastAPI(
    title="NoteManager API",
    description="A simple CRUD API to manage notes using FastAPI and SQLAlchemy",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    """
    Root endpoint of the NoteManager API.
    Returns a welcome message.
    """
    logger.info("Root endpoint '/' was accessed.")
    return JSONResponse(content={"msg": "Welcome to the NoteManager API."})

# Register all API routers
app.include_router(auth_router, prefix="", tags=["Auth"])  
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(note_router, prefix="/notes", tags=["Notes"])

logger.info("Routes for auth, users and note registered. App Ready.")
