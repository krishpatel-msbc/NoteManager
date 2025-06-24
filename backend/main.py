from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.db.database import engine
from backend.models.base import Base
from backend.models.user import User
from backend.models.note import Note, Tag
from backend.api.route_user import router as user_router
from backend.api.route_note import router as note_router
from backend.api.route_auth import router as auth_router 

from dotenv import load_dotenv
import os

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NoteManager API",
    description="A simple CRUD API to manage notes using FastAPI and SQLAlchemy",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return JSONResponse(content={"msg":"Welcome to the NoteManager API"})

app.include_router(auth_router, prefix="", tags=["Auth"])  
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(note_router, prefix="/notes", tags=["Notes"])


