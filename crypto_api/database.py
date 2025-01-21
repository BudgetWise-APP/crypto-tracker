from motor.motor_asyncio import AsyncIOMotorClient
from crypto_api.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client.crypto_api_database
