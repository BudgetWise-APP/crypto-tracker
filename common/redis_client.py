import redis
from .config import REDIS_HOST, REDIS_PASSWORD

redis_client = redis.Redis(
    host=REDIS_HOST, port=6379, password=REDIS_PASSWORD, ssl=True
)
