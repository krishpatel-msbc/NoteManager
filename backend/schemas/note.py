from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timezone



class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None

class NoteCreate(NoteBase):
    tags: Optional[List[TagCreate]] = []

class NoteUpdate(NoteBase):
    tags: Optional[List[TagCreate]] = []

class NoteInDBBase(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[Tag] = []

    class Config:
        orm_mode = True

class Note(NoteInDBBase):
    pass


