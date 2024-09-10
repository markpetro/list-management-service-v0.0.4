from celery import Celery
from app.database import Database
from app.models import ListItem
from app.database import session_scope

# Initialize Celery app with Redis as the broker
celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def send_registration_email(user_email):
    # Logic to send registration email to the user
    print(f"Email sent to {user_email}")


@celery.task
def sync_to_postgres(list_id, value, action, comment, author):
    """Syncs values to PostgreSQL asynchronously."""
    db = Database()

    with session_scope() as session:
        if action == "add":
            db.add_list_item(list_id, value, comment, author)
        elif action == "edit":
            old_value = "some_old_value"  # Replace with actual logic to fetch old value
            db.update_list_item(list_id, old_value, value, comment, author)
        elif action == "delete":
            db.delete_list_item(list_id, value)

    print(f"Action {action} performed on list {list_id} for value {value} by {author}.")


@celery.task
def bulk_add_task(list_id, values, comment, author, role):
    """Bulk add task."""
    with session_scope() as session:
        try:
            for value in values:
                list_item = ListItem(list_id=list_id, value=value, comment=comment, created_by=author)
                session.add(list_item)
            session.commit()
            return f"Bulk add: {len(values)} items added to list {list_id}"
        except Exception as e:
            session.rollback()  # Rollback on error
            print(f"Error adding items: {str(e)}")
            return f"Error: {str(e)}"


@celery.task
def bulk_delete_task(list_id, values, role):
    """Bulk delete task."""
    with session_scope() as session:
        try:
            session.query(ListItem).filter(ListItem.list_id == list_id, ListItem.value.in_(values)).update(
                {"is_deleted": True})
            session.commit()
            return f"Bulk delete: {len(values)} items deleted from list {list_id}"
        except Exception as e:
            session.rollback()  # Rollback on error
            print(f"Error deleting items: {str(e)}")
            return f"Error: {str(e)}"