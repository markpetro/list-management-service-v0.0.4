import logging
from datetime import datetime
from app.database import Database
from app.services.notification_service import NotificationService
from app.utils.redis_cache import RedisCache
from app.tasks.celery_tasks import sync_to_postgres
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import exc as orm_exc
from app.utils.logging_service import logger

def add_value(self, list_id, value, comment, author, role):
    try:
        self.check_permission(role, 'add')
        list_type = self.db.get_list_by_id(list_id).type
        self.validate_value(value, list_type)

        if self.redis_client.exists(f"{list_type}:{value}") or self.db.check_value_in_list(list_type, value):
            logger.log_warning(f"Duplicate value: {value} attempt in list: {list_type}")
            raise ValueError("Value already exists in the list")

        self._cache_value(list_type, value, 'set')
        sync_to_postgres.delay(list_id, value, 'add', comment, author)

        logger.log_info(f"Added value: {value} to list ID: {list_id}")
        return {"status": "Added successfully"}
    except (IntegrityError, ValidationError, PermissionError, ValueError) as e:
        logger.log_error(f"Error adding value: {value} to list ID: {list_id} - {str(e)}")
        return {"error": str(e)}


class ValidationError(Exception):
    pass

class PermissionError(Exception):
    pass

class ListManagementService:
    def __init__(self, db: Database = None, redis_client: RedisCache = None, notification_service: NotificationService = None):
        self.db = db or Database()
        self.redis_client = redis_client or RedisCache()
        self.notification_service = notification_service or NotificationService()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # Define role-based permissions
        self.roles_permissions = {
            'admin': ['add', 'edit', 'delete', 'bulk_add', 'bulk_delete', 'change_type', 'view'],
            'editor': ['add', 'edit', 'bulk_add', 'bulk_delete', 'view'],
            'viewer': ['view']
        }

    def log_action(self, action, user, details):
        """Log user actions."""
        timestamp = datetime.utcnow().isoformat()
        self.logger.info(f"{timestamp} - User: {user}, Action: {action}, Details: {details}")

    def check_permission(self, role, action):
        """Check if the user role has permission for the specified action."""
        if action not in self.roles_permissions.get(role, []):
            raise PermissionError(f"Role '{role}' does not have permission to perform '{action}'.")

    def validate_value(self, value, list_type):
        """Validate the length and characters of the value."""
        if len(value) > 255:
            raise ValidationError("Value exceeds the maximum length of 255 characters.")
        if not value.isalnum():
            raise ValidationError("Value contains invalid characters. Only alphanumeric characters are allowed.")

    def _cache_key(self, list_type, value):
        """Generate the Redis cache key."""
        return f"{list_type}:{value}"

    def _check_in_cache(self, list_type, value):
        """Check if the value exists in Redis cache."""
        return self.redis_client.exists(self._cache_key(list_type, value))

    def _cache_value(self, list_type, value):
        """Cache the value in Redis."""
        self.redis_client.set(self._cache_key(list_type, value), 'cached')

    def _remove_from_cache(self, list_type, value):
        """Remove a value from Redis cache."""
        self.redis_client.delete(self._cache_key(list_type, value))

    def check_value(self, list_type, value, role):
        """Check if a value exists in the list, using Redis first."""
        try:
            self.check_permission(role, 'view')
            self.validate_value(value, list_type)

            redis_key = self._cache_key(list_type, value)
            exists = self._check_in_cache(list_type, value)

            if not exists:
                exists = self.db.check_value_in_list(list_type, value)
                if exists:
                    self._cache_value(list_type, value)

            self.log_action('check_value', 'system', f"Checked value '{value}' in list '{list_type}'")
            return exists
        except (ValidationError, PermissionError) as e:
            return {"error": str(e)}

    def add_value(self, list_id, value, comment, author, role):
        """Add a value to the list and sync it to PostgreSQL."""
        try:
            self.check_permission(role, 'add')
            list_type = self.db.get_list_by_id(list_id).type
            self.validate_value(value, list_type)

            if self._check_in_cache(list_type, value) or self.db.check_value_in_list(list_type, value):
                self.notification_service.send_slack_notification(f"Duplicate value attempt: {value} in list {list_type}")
                raise ValueError("Value already exists in the list")

            self._cache_value(list_type, value)
            sync_to_postgres.delay(list_id, value, 'add', comment, author)

            self.log_action('add_value', author, f"Added value '{value}' to list '{list_id}'")
            return {"status": "Added successfully"}
        except (IntegrityError, ValidationError, PermissionError, ValueError) as e:
            return {"error": str(e)}

    def bulk_add_values(self, list_id, values, comment, author, role):
        """Bulk add values to the list."""
        try:
            self.check_permission(role, 'bulk_add')
            list_type = self.db.get_list_by_id(list_id).type
            added_values, errors = [], []

            for value in values:
                try:
                    self.validate_value(value, list_type)
                    if not self._check_in_cache(list_type, value) and not self.db.check_value_in_list(list_type, value):
                        self._cache_value(list_type, value)
                        added_values.append(value)
                        sync_to_postgres.delay(list_id, value, 'add', comment, author)
                    else:
                        errors.append(f"Value '{value}' already exists.")
                except ValidationError as e:
                    errors.append(str(e))

            self.log_action('bulk_add_values', author, f"Bulk added values to list '{list_id}'")
            if errors:
                return {"status": "Partial success", "added_values": added_values, "errors": errors}
            return {"status": "All values added successfully", "added_values": added_values}
        except PermissionError as e:
            return {"error": str(e)}

    def edit_value(self, list_id, old_value, new_value, comment, author, role):
        """Edit an existing value in the list."""
        try:
            self.check_permission(role, 'edit')
            list_type = self.db.get_list_by_id(list_id).type
            self.validate_value(new_value, list_type)

            if self._check_in_cache(list_type, new_value) or self.db.check_value_in_list(list_type, new_value):
                raise ValueError("New value already exists in the list")

            self._remove_from_cache(list_type, old_value)
            self._cache_value(list_type, new_value)

            sync_to_postgres.delay(list_id, new_value, 'edit', comment, author)

            self.log_action('edit_value', author, f"Edited value from '{old_value}' to '{new_value}' in list '{list_id}'")
            return {"status": "Value edited successfully"}
        except (orm_exc.NoResultFound, IntegrityError, ValidationError, PermissionError, ValueError) as e:
            return {"error": str(e)}

    def delete_value(self, list_id, value, role):
        """Delete a value from the list."""
        try:
            self.check_permission(role, 'delete')
            list_type = self.db.get_list_by_id(list_id).type

            if not self._check_in_cache(list_type, value) and not self.db.check_value_in_list(list_type, value):
                raise ValueError("Value does not exist in the list")

            self._remove_from_cache(list_type, value)
            sync_to_postgres.delay(list_id, value, 'delete', '', 'system')

            self.log_action('delete_value', 'system', f"Deleted value '{value}' from list '{list_id}'")
            return {"status": "Deleted successfully"}
        except (orm_exc.NoResultFound, IntegrityError, PermissionError, ValueError) as e:
            return {"error": str(e)}

    def bulk_delete_values(self, list_id, values, role):
        """Bulk delete values from the list."""
        try:
            self.check_permission(role, 'bulk_delete')
            list_type = self.db.get_list_by_id(list_id).type
            deleted_values, errors = [], []

            for value in values:
                try:
                    if self._check_in_cache(list_type, value) or self.db.check_value_in_list(list_type, value):
                        self._remove_from_cache(list_type, value)
                        deleted_values.append(value)
                        sync_to_postgres.delay(list_id, value, 'delete', '', 'system')
                    else:
                        errors.append(f"Value '{value}' does not exist.")
                except Exception as e:
                    errors.append(str(e))

            self.log_action('bulk_delete_values', 'system', f"Bulk deleted values from list '{list_id}'")
            if errors:
                return {"status": "Partial success", "deleted_values": deleted_values, "errors": errors}
            return {"status": "All values deleted successfully"}
        except PermissionError as e:
            return {"error": str(e)}

    def change_list_type(self, list_id, new_type, role):
        """Change the type of a list."""
        try:
            self.check_permission(role, 'change_type')
            self.db.update_list_type(list_id, new_type)
            self.log_action('change_list_type', 'system', f"Changed list type for list '{list_id}' to '{new_type}'")
            return {"status": "List type updated successfully"}
        except (orm_exc.NoResultFound, PermissionError) as e:
            return {"error": str(e)}