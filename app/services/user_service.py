"""
DushimeMart - User Service (business logic for user registration & authentication)
Author: Cleonide Dushime (ID: 70871)
"""
from typing import Optional

from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserRegister
from app.security import hash_password, verify_password


class UserService:
    """Encapsulates business logic for users — kept separate from HTTP layer."""

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def register(db: Session, payload: UserRegister) -> Optional[User]:
        """Create a new user. Returns None if email already exists."""
        if UserService.get_by_email(db, payload.email):
            return None

        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        """Return the user if credentials are valid, otherwise None."""
        user = UserService.get_by_email(db, email)
        if user and verify_password(password, user.hashed_password):
            return user
        return None
