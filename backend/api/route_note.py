"""
API routes for managing notes.

This module defines endpoints to create, read, and list notes for authenticated users.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.schemas.note import Note, NoteCreate
from backend.models.note import Note as NoteModel
from backend.core.deps import get_current_user 
from backend.models.user import User 
from backend.logger import logger  # Logger for info and error tracking

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model=Note)
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new note for the current authenticated user.

    - Creates new tags if they do not exist.
    - Associates tags with the note.
    """
    logger.info(f"Creating a note for user_id={current_user.id} with title='{note.title}'")
    db_note = NoteModel(**note.dict(exclude={"tags"}), owner_id=current_user.id)

    if note.tags:
        tags = []
        for tag_in in note.tags:
            tag = db.query(NoteModel.tags.property.mapper.class_).filter_by(name=tag_in.name).first()
            if not tag:
                logger.info(f"Creating new tag '{tag_in.name}' for note")
                tag = NoteModel.tags.property.mapper.class_(name=tag_in.name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            tags.append(tag)
        db_note.tags = tags

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    logger.info(f"Note created successfully with id={db_note.id}")
    return db_note

@router.get("/{note_id}", response_model=Note)
def read_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve a specific note by its ID for the current authenticated user.

    Raises 404 if note does not exist or does not belong to user.
    """
    logger.info(f"Fetching note id={note_id} for user_id={current_user.id}")
    db_note = db.query(NoteModel).filter(NoteModel.id == note_id, NoteModel.owner_id == current_user.id).first()
    if not db_note:
        logger.warning(f"Note id={note_id} not found for user_id={current_user.id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    logger.info(f"Note id={note_id} retrieved for user_id={current_user.id}")
    return db_note

@router.get("/", response_model=list[Note])
def read_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve a list of notes for the current authenticated user.

    Supports pagination via skip and limit query parameters.
    """
    logger.info(f"Fetching notes for user_id={current_user.id} with skip={skip} and limit={limit}")
    notes = db.query(NoteModel).filter(NoteModel.owner_id == current_user.id).offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(notes)} notes for user_id={current_user.id}")
    return notes
