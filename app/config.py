#config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = os.getenv("DB_NAME")

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")

    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Fallback if env var is not set
    ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Fallback if env var is not set
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()