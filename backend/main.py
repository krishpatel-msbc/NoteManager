"""
Main application entrypoint for the NoteManager API.
Initializes the FastAPI app, includes routes, and handles startup/shutdown logging.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from backend.api.route_user import router as user_router
from backend.api.route_note import router as note_router
from backend.api.route_auth import router as auth_router 
from backend.logger import logger
from dotenv import load_dotenv
import threading
from backend.utils.api_notifier import api_call_worker

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("NoteManager API is starting up...")
    thread = threading.Thread(target=api_call_worker, daemon=True)
    thread.start()
    yield
    logger.info("NoteManager API is shutting down...")

app = FastAPI(
    title="NoteManager API",
    description="A simple CRUD API to manage notes using FastAPI and SQLAlchemy",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    logger.info("Root endpoint '/' was accessed.")
    return JSONResponse(content={"msg": "Welcome to the NoteManager API."})

# Register routers
app.include_router(user_router)
app.include_router(note_router)
app.include_router(auth_router)

logger.info("Routes registered. App Ready.")
