from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas import user as user_schema
from backend.crud import user as user_crud
from backend.db.database import get_db
from backend.core.deps import get_current_user  # new
from backend.models.user import User  # new

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=user_schema.User)
def create_user(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db, user_in=user_in)

@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=user_schema.User)
def update_user(user_id: int, user_in: user_schema.UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_crud.update_user(db, user=user, user_in=user_in)
