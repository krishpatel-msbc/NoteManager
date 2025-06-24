from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.schemas.note import Note, NoteCreate
from backend.models.note import Note as NoteModel
from backend.core.deps import get_current_user 
from backend.models.user import User 

router = APIRouter(prefix="/notes",tags=["Notes"],)

@router.post("/", response_model=Note)
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = NoteModel(**note.dict(exclude={"tags"}), owner_id=current_user.id)
    # Handle tags in crud usually, but simplified here:
    if note.tags:
        tags = []
        for tag_in in note.tags:
            tag = db.query(NoteModel.tags.property.mapper.class_).filter_by(name=tag_in.name).first()
            if not tag:
                tag = NoteModel.tags.property.mapper.class_(name=tag_in.name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            tags.append(tag)
        db_note.tags = tags

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/{note_id}", response_model=Note)
def read_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = db.query(NoteModel).filter(NoteModel.id == note_id, NoteModel.owner_id == current_user.id).first()
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return db_note

@router.get("/", response_model=list[Note])
def read_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notes = db.query(NoteModel).filter(NoteModel.owner_id == current_user.id).offset(skip).limit(limit).all()
    return notes
