from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models.note import Note, Tag
from backend.schemas.note import NoteCreate, NoteUpdate, TagCreate
from backend.logger import logger


def get_note(db: Session, note_id: int) -> Optional[Note]:
    logger.info(f"Fetching note with id={note_id}")
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        logger.info(f"Found note with id={note_id}")
    else:
        logger.warning(f"Note with id={note_id} not found")
    return note

def get_notes(db: Session, skip: int = 0, limit: int = 100) -> List[Note]:
    logger.info(f"Fetching notes with skip={skip}, limit= {limit}")
    notes = db.query(Note).offset(skip).limit(limit).all()
    logger.info(f"Fetched {len(notes)} notes")
    return notes


def create_note(db: Session, note_in: NoteCreate, owner_id: int) -> Note:
    logger.info(f"Creating note titled '{note_in.title}' for owner_id={owner_id}")
    tags = []
    try:
        for tag_in in note_in.tags or []:
            tag = db.query(Tag).filter(Tag.name == tag_in.name).first()
            if not tag:
                logger.info(f"Tag '{tag_in.name}' not found, creating new tag")
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
        logger.info(f"Note created with id={db_note.id}")
        return db_note
    except Exception as e:
        logger.error(f"Error creating note titled '{note_in.title}': {e}", exc_info=True)
        db.rollback()
        raise


def update_note(db: Session, note: Note, note_in: NoteUpdate) -> Note:
    logger.info(f"Updating note id={note.id}")
    try:
        note.title = note_in.title
        note.content = note_in.content

        if note_in.tags is not None:
            tags = []
            for tag_in in note_in.tags:
                tag = db.query(Tag).filter(Tag.name == tag_in.name).first()
                if not tag:
                    logger.info(f"Tag '{tag_in.name}' not found, creating new tag")
                    tag = Tag(name=tag_in.name)
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)
                tags.append(tag)
            note.tags = tags

        db.add(note)
        db.commit()
        db.refresh(note)
        logger.info(f"Note id={note.id} updated successfully")
        return note
    except Exception as e:
        logger.error(f"Error updating note id={note.id}: {e}", exc_info=True)
        db.rollback()
        raise


def delete_note(db: Session, note: Note) -> None:
    logger.info(f"Deleting note id={note.id}")
    try:
        db.delete(note)
        db.commit()
        logger.info(f"Note id={note.id} deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting note id={note.id}: {e}", exc_info=True)
        db.rollback()
        raise