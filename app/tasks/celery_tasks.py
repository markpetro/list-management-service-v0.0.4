from celery import Celery
from app.database import Database  # Import the database class to perform database operations

# Initialize Celery app with Redis as the broker
celery = Celery('tasks', broker='redis://localhost:6379/0')


# Define sync_to_postgres task
@celery.task
def sync_to_postgres(list_id, value, action, comment, author):
    """
    This task handles syncing values to the PostgreSQL database asynchronously.
    """
    db = Database()  # Initialize a database connection

    if action == "add":
        db.add_list_item(list_id, value, comment, author)
    elif action == "edit":
        # Assuming you have some logic to fetch old_value for editing
        old_value = "some_old_value"  # Replace this with actual logic
        db.update_list_item(list_id, old_value, value, comment, author)
    elif action == "delete":
        db.delete_list_item(list_id, value)

    # You can log or print the operation
    print(f"Action {action} performed on list {list_id} for value {value} by {author}.")


@celery.task
def bulk_add_task(list_id, values, comment, author, role):
    # Bulk add logic here
    pass

@celery.task
def bulk_delete_task(list_id, values, role):
    # Bulk delete logic here
    pass