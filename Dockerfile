# Use official Python image as a base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies, PostgreSQL development libraries, and PostgreSQL client tools
# Also install netcat-traditional for network checks
RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y libpq-dev gcc netcat-traditional postgresql-client && \
    pip install --no-cache-dir -r requirements.txt

# Make sure Uvicorn is installed
RUN pip install uvicorn

# Create a non-root user and group for Celery
RUN groupadd -r celery && useradd -r -g celery celery

# Change ownership of /app directory to the non-root user
RUN chown -R celery:celery /app

# Set executable permissions for entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the port FastAPI will run on
EXPOSE 8000

# By default, run the FastAPI application with Uvicorn
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]