import redis.asyncio as redis

redis_client = None


async def init_redis():
    global redis_client
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    print(f"Redis connection initialized {await redis_client.ping()}")


def get_redis_client():
    if redis_client is None:
        raise RuntimeError("Redis client not initialized. Call init_redis() first.")
    return redis_client
