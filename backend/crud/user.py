"""
CRUD operations for users.

Handles user creation, retrieval, updating, and password verification.
"""

from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from backend.logger import logger

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash a plain text password.

    Args:
        password (str): The user's password in plain text.

    Returns:
        str: The hashed password.
    """
    logger.debug("Hashing Password")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against its hash.

    Args:
        plain_password (str): Plain text password.
        hashed_password (str): Hashed password stored in DB.

    Returns:
        bool: True if valid, else False.
    """
    logger.debug("Veryfing Password")
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, user_id: int) -> User | None:
    """
    Retrieve a user by ID.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user to fetch.

    Returns:
        User | None: User object if found, otherwise None.
    """
    logger.info(f"Fetching user with id={user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        logger.info(f"User Found: id={user.id}, username={user.username}")
    else:
        logger.warning(f"User not found with id = {user_id}")
    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retrieve a user by email address.

    Args:
        db (Session): SQLAlchemy database session.
        email (str): Email address to look up.

    Returns:
        User | None: User object if found, otherwise None.
    """
    logger.info(f"Looking up user by email: {email}")
    user = db.query(User).filter(User.email == email).first()
    if user:
        logger.info(f"User found with email: {email}")
    else:
        logger.warning(f"No user found with email: {email}")
    return user 

def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Retrieve a user by username.

    Args:
        db (Session): SQLAlchemy database session.
        username (str): Username to look up.

    Returns:
        User | None: User object if found, otherwise None.
    """
    logger.info(f"Looking up user by username: {username}")
    user = db.query(User).filter(User.username == username).first()
    if user:
        logger.info(f"User found with username: {username}")
    else:
        logger.warning(f"No user found with username: {username}")
    return user

def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db (Session): SQLAlchemy database session.
        user_in (UserCreate): User creation data.

    Returns:
        User: The newly created user object.
    """
    logger.info(f"Creating user with username: {user_in.username}")
    try:
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User created successfully with id = {db_user.id}")
        return db_user
    except Exception as e:
        logger.error(f"Failed to create user: {e}", exc_info=True)
        db.rollback()
        raise

def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    """
    Update an existing user's information.

    Args:
        db (Session): SQLAlchemy database session.
        user (User): The user object to update.
        user_in (UserUpdate): Updated user data.

    Returns:
        User: The updated user object.
    """
    logger.info(f"Updating user id={user.id}")
    try:
        if user_in.username is not None:
            logger.debug(f"Updating username to: {user_in.username}")
            user.username = user_in.username
        if user_in.email is not None:
            logger.debug(f"Updating email to: {user_in.email}")
            user.email = user_in.email
        if user_in.password is not None:
            logger.debug("Updating password")
            user.hashed_password = get_password_hash(user_in.password)

        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User updated successfully: id={user.id}")
        return user
    except Exception as e:
        logger.error(f"Failed to update user id={user.id}: {e}", exc_info=True)
        db.rollback()
        raise
