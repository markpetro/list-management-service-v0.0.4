# app/database.py
from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import IntegrityError, NoResultFound
from contextlib import contextmanager
import redis
import os
from dotenv import load_dotenv
import logging

from app.models import User, List, ListItem  # Only import models here
from app.db_setup import Base, SessionLocal  # Import Base and SessionLocal from db_setup.py

# Initialize logger
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Redis connection
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
REDIS_URL = f"redis://{redis_host}:{redis_port}/0"

# Scoped session
Session = scoped_session(SessionLocal)

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Session rollback due to: {e}")
        raise
    finally:
        session.close()


class Database:
    def __init__(self):
        self.redis = redis.StrictRedis.from_url(REDIS_URL)  # Redis client

    def create_tables(self):
        """Create database tables."""
        Base.metadata.create_all(SessionLocal().get_bind())

    # The rest of your methods go here...