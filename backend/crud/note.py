from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models.note import Note, Tag
from backend.schemas.note import NoteCreate, NoteUpdate, TagCreate

def get_note(db: Session, note_id: int) -> Optional[Note]:
    return db.query(Note).filter(Note.id == note_id).first()

def get_notes(db: Session, skip: int = 0, limit: int = 100) -> List[Note]:
    return db.query(Note).offset(skip).limit(limit).all()

def create_note(db: Session, note_in: NoteCreate, owner_id: int) -> Note:
    tags = []
    for tag_in in note_in.tags or []:
        tag = db.query(Tag).filter(Tag.name == tag_in.name).first()
        if not tag:
            tag = Tag(name=tag_in.name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tags.append(tag)

    db_note = Note(
        title=note_in.title,
        content=note_in.content,
        owner_id=owner_id,
        tags=tags
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note: Note, note_in: NoteUpdate) -> Note:
    note.title = note_in.title
    note.content = note_in.content

    if note_in.tags is not None:
        tags = []
        for tag_in in note_in.tags:
            tag = db.query(Tag).filter(Tag.name == tag_in.name).first()
            if not tag:
                tag = Tag(name=tag_in.name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            tags.append(tag)
        note.tags = tags

    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note: Note) -> None:
    db.delete(note)
    db.commit()