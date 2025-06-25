"""
API routes for authentication.

Includes login endpoint to obtain JWT access tokens.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.crud import user as user_crud
from backend.core.security import create_access_token, verify_password
from backend.schemas.token import Token
from backend.logger import logger  # Logger for login attempts and errors

router = APIRouter(tags=["Auth"])

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT access token.

    Validates email and password, returns token if successful.
    """
    logger.info(f"Login attempt for: {form_data.username}")
    user = user_crud.get_user_by_email(db, email=form_data.username)

    if not user:
        logger.warning(f"Login failed: user with email {form_data.username} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed: incorrect password for user {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Login successful for user: {user.email}")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
