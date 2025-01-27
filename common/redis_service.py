import json
import redis
from .config import REDIS_HOST, REDIS_PASSWORD

redis_client = redis.Redis(
    host=REDIS_HOST, port=6379, password=REDIS_PASSWORD, ssl=True
)

class CacheService:
    @staticmethod
    async def get_data_from_redis(redis_key: str):
        cached_data = redis_client.get(redis_key)
        if cached_data:
            print("Data fetched from Redis")
            return json.loads(cached_data)
        return None

    @staticmethod
    async def set_data_to_redis(redis_key: str, data: dict, ttl: int = 86400):
        redis_client.set(redis_key, data, ex=ttl)
        print(f"Data cached in Redis with TTL: {ttl} seconds")