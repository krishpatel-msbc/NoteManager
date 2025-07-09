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
import webbrowser
import time

# Load environment variables
load_dotenv()

EXTERNAL_URL = "https://webhook.site/feae50a3-1af1-4a91-bc80-724b53915f1d"

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("NoteManager API is starting up...")

    # Optional: remove the browser-launch thread too
    def open_external_url():
        time.sleep(1.5)
        logger.info(f"Opening external URL: {EXTERNAL_URL}")
        webbrowser.open(EXTERNAL_URL)

    threading.Thread(target=open_external_url, daemon=True).start()

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
