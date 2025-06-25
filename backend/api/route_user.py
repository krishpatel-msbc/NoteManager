from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas import user as user_schema
from backend.crud import user as user_crud
from backend.db.database import get_db
from backend.core.deps import get_current_user
from backend.models.user import User
from backend.logger import logger  # ✅ Add logger

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=user_schema.User)
def create_user(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to create user with email: {user_in.email}")
    db_user = user_crud.get_user_by_email(db, email=user_in.email)
    if db_user:
        logger.warning(f"User creation failed: Email already registered - {user_in.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    user = user_crud.create_user(db, user_in=user_in)
    logger.info(f"User created successfully: id={user.id}, email={user.email}")
    return user

@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"Fetching user with id={user_id}")
    db_user = user_crud.get_user(db, user_id=user_id)
    if not db_user:
        logger.warning(f"User not found with id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User fetched: id={db_user.id}, username={db_user.username}")
    return db_user

@router.put("/{user_id}", response_model=user_schema.User)
def update_user(user_id: int, user_in: user_schema.UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"Attempting to update user id={user_id}")
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        logger.warning(f"User not found for update: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = user_crud.update_user(db, user=user, user_in=user_in)
    logger.info(f"User updated: id={updated_user.id}, username={updated_user.username}")
    return updated_user
