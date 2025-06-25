"""
Schemas for token-based authentication responses and validation.
"""

from pydantic import BaseModel

class Token(BaseModel):
    """
    Schema for returned JWT access tokens.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for JWT payload extraction/validation.
    """
    email: str | None = None # Optional email from token's "sub" claim
