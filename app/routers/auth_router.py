"""
DushimeMart - Auth Router (controller layer for /auth endpoints)
Author: Cleonide Dushime (ID: 70871)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TokenResponse, UserLogin, UserRegister, UserResponse
from app.security import create_access_token
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new customer account",
)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """Create a new user account. Returns 400 if email is already in use."""
    user = UserService.register(db, payload)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in and receive a JWT access token",
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """Authenticate with email + password and receive a Bearer token."""
    user = UserService.authenticate(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token)
