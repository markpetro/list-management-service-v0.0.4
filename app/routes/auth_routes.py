# auth_routes.py
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db_setup import get_db
from app.services.auth_service import create_access_token, authenticate_user, register_new_user
from app.schemas import Token, UserLogin, UserCreate
from app.utils.jwt_auth import get_current_user

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/register", response_model=UserCreate)
def register(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Registering user: {user.username}")
    registered_user = register_new_user(user, db)
    return registered_user


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for user: {user.username}")
    authenticated_user = authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        logger.warning(f"Failed login attempt for user: {user.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": authenticated_user.username})
    logger.info(f"User {user.username} logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserCreate)
def read_users_me(current_user=Depends(get_current_user)):
    logger.info(f"Reading current user: {current_user.username}")
    return current_user
