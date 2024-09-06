from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api_gateway import router as api_gateway_router
from fastapi_limiter import FastAPILimiter
import os
import redis.asyncio as redis  # Correct usage for async Redis connections

# Use Docker service name 'redis' to connect to Redis within Docker
redis_host = os.getenv('REDIS_HOST', 'redis')  # 'redis' is the Docker service name
redis_port = os.getenv('REDIS_PORT', '6379')
redis_url = f"redis://{redis_host}:{redis_port}/0"

# Initialize FastAPI app
app = FastAPI()

# Serve static frontend files from the 'frontend' directory
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Include the API Gateway router
app.include_router(api_gateway_router, prefix="/api", tags=["API Gateway"])

# Initialize Redis for rate limiting
@app.on_event("startup")
async def startup():
    redis_client = redis.from_url(redis_url, decode_responses=True)  # Async Redis client using redis.asyncio
   # await FastAPILimiter.init(redis_client)  # Initialize FastAPI rate limiter with Redis

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the List Management API"}