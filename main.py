from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import router
from redis_config import init_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_redis()
        print("Redis initialized")
    except Exception as e:
        print(f"Redis init failed: {e}")
    yield
    print("Redis connection closed")


app = FastAPI(lifespan=lifespan)

# Register routes
app.include_router(router)
