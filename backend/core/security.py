"""
Provides security related functions for the app inlucing:-
Password Hashing and Verification
JWT creation and decoding
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from backend.core.config import settings

# Setup password hashing using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 #Token validity in minutes

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies whether the plain password matches the hashed version.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a password using bcrypt.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a signed JWT access token with an optional expiration.
    
    Args:
        data: Payload data (should include 'sub' field for user identity).
        expires_delta: Optional timedelta to override default expiration.
    
    Returns:
        Encoded JWT token as a string."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodes a JWT token. Returns payload if valid, else None.
    
    Args:
        token: JWT token string.
    
    Returns:
        Decoded payload dictionary or None if token is invalid.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
