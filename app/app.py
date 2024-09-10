#app.py
import os
import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from app.celery_app import celery_app
from app.routes import list_routes, report_routes, user_routes, auth_routes
from app.config import settings
from app.api_gateway import router as api_gateway_router


# CORS configuration: Allow requests from your frontend
origins = [
    "http://localhost:5173",  # Frontend URL during development
    # Add more origins as necessary
]

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Register routes for various modules
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(list_routes.router, prefix="/list", tags=["List"])
app.include_router(report_routes.router, prefix="/report", tags=["Report"])
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(api_gateway_router, prefix="/api", tags=["API Gateway"])


# Celery example task
@celery_app.task
def example_task():
    return "Task completed"


# Initialize Redis for rate limiting
async def initialize_redis():
    redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
    redis_client = redis.from_url(redis_url, decode_responses=True)
    await FastAPILimiter.init(redis_client)


# Avoid circular dependencies by dynamically including routers
def include_routers(app: FastAPI):
    from app.api_gateway import router as api_gateway_router
    app.include_router(api_gateway_router, prefix="/api", tags=["API Gateway"])


include_routers(app)


# Initialize Redis on app startup for rate limiting
@app.on_event("startup")
async def startup():
    await initialize_redis()


# Root endpoint for basic welcome message
@app.get("/")
async def root():
    return {"message": "Welcome to the List Management API"}
