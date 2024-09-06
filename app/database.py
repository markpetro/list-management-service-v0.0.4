from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, scoped_session
from app.models import Base, List, ListItem  # Import models from app.models
import redis
import os
from dotenv import load_dotenv
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError, NoResultFound
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Database connection URL
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Redis connection
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')

REDIS_URL = f"redis://{redis_host}:{redis_port}/0"

# SQLAlchemy engine and session setup
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))


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
        Base.metadata.create_all(engine)

    def get_list_by_id(self, list_id):
        """Fetch a list by its ID."""
        with session_scope() as session:
            return session.query(List).filter(List.id == list_id, List.is_deleted == False).one_or_none()

    def check_value_in_list(self, list_type, value):
        """Check if a value exists in the list using Redis caching for hot data."""
        cache_key = f"{list_type}:{value}"
        cached_result = self.redis.get(cache_key)
        if cached_result is not None:
            return cached_result == b'True'

        # Query PostgreSQL if not found in Redis cache
        with session_scope() as session:
            exists = session.query(ListItem).join(List).filter(
                and_(
                    List.type == list_type,
                    ListItem.value == value,
                    List.is_deleted == False,
                    ListItem.is_deleted == False
                )
            ).count() > 0

            # Cache the result in Redis for 1 hour
            self.redis.set(cache_key, str(exists), ex=3600)
            return exists

    def add_list_item(self, list_id, value, comment, author):
        """Add a new item to the list and invalidate the Redis cache for this value."""
        new_item = ListItem(list_id=list_id, value=value, comment=comment, created_by=author)
        with session_scope() as session:
            try:
                session.add(new_item)

                # Invalidate the cache for the newly added value
                list_type = self.get_list_by_id(list_id).type
                cache_key = f"{list_type}:{value}"
                self.redis.delete(cache_key)
                logger.info(f"Added new item to list {list_id} and invalidated cache for {value}")

            except IntegrityError as e:
                logger.error(f"Integrity error when adding list item: {e}")
                raise

    def update_list_item(self, list_id, old_value, new_value, comment, author):
        """Update a list item and invalidate the Redis cache for both the old and new values."""
        with session_scope() as session:
            try:
                item = session.query(ListItem).filter(
                    and_(
                        ListItem.list_id == list_id,
                        ListItem.value == old_value,
                        ListItem.is_deleted == False
                    )
                ).one()

                item.value = new_value
                item.comment = comment
                item.updated_by = author

                # Invalidate cache for old and new values
                list_type = self.get_list_by_id(list_id).type
                self.redis.delete(f"{list_type}:{old_value}")
                self.redis.delete(f"{list_type}:{new_value}")

                logger.info(f"Updated item in list {list_id} from {old_value} to {new_value} and invalidated cache")

            except NoResultFound:
                logger.error(f"Item not found in list {list_id} for value {old_value}")
                raise
            except IntegrityError as e:
                logger.error(f"Integrity error when updating list item: {e}")
                raise

    def delete_list_item(self, list_id, value):
        """Delete a list item and invalidate the Redis cache for the deleted value."""
        with session_scope() as session:
            try:
                item = session.query(ListItem).filter(
                    and_(
                        ListItem.list_id == list_id,
                        ListItem.value == value,
                        ListItem.is_deleted == False
                    )
                ).one()

                item.is_deleted = True

                # Invalidate cache for the deleted value
                list_type = self.get_list_by_id(list_id).type
                self.redis.delete(f"{list_type}:{value}")
                logger.info(f"Deleted item from list {list_id} for value {value} and invalidated cache")

            except NoResultFound:
                logger.error(f"Item not found for deletion in list {list_id} for value {value}")
                raise
            except IntegrityError as e:
                logger.error(f"Integrity error when deleting list item: {e}")
                raise

    def update_list_type(self, list_id, new_type):
        """Update the list type and invalidate the Redis cache for all values in the list."""
        with session_scope() as session:
            try:
                list_obj = self.get_list_by_id(list_id)
                if list_obj:
                    old_type = list_obj.type
                    list_obj.type = new_type

                    # Invalidate all cached values for the old list type
                    self.invalidate_cache_for_list(list_id, old_type)

                    logger.info(f"Updated list {list_id} type from {old_type} to {new_type}")
                    return {"status": "List type updated successfully"}
                else:
                    logger.error(f"List {list_id} not found for type update")
                    return {"error": "List not found"}

            except NoResultFound:
                logger.error(f"List {list_id} not found")
                raise
            except IntegrityError as e:
                logger.error(f"Integrity error when updating list type: {e}")
                raise

    def invalidate_cache_for_list(self, list_id, old_type):
        """Invalidate all Redis cache entries for a given list."""
        with session_scope() as session:
            items = session.query(ListItem).filter(ListItem.list_id == list_id, ListItem.is_deleted == False).all()
            for item in items:
                self.redis.delete(f"{old_type}:{item.value}")
                logger.info(f"Invalidated cache for item {item.value} in list {list_id} with old type {old_type}")

    def get_list_items_paginated(self, list_id, page=1, per_page=20):
        """Retrieve paginated list items."""
        offset = (page - 1) * per_page
        with session_scope() as session:
            items_query = session.query(ListItem).filter(
                and_(
                    ListItem.list_id == list_id,
                    ListItem.is_deleted == False
                )
            ).offset(offset).limit(per_page)

            total_count = session.query(ListItem).filter(
                and_(
                    ListItem.list_id == list_id,
                    ListItem.is_deleted == False
                )
            ).count()

        return items_query.all(), total_count