from dotenv import load_dotenv
import os

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
CONSUMER_GROUP = os.getenv('CONSUMER_GROUP')
MONGO_URI = os.getenv('MONGO_URI')
COINMAKERCAP_TOKEN = os.getenv('COINMAKERCAP_TOKEN')
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"
ORIGINS = [
    'http://localhost:8899',
    'http://10.0.11.165:8899',
    'http://10.2.0.2:8899',
    'https://budgetwise-chi.vercel.app',
]
