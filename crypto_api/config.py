from dotenv import load_dotenv
import os

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
CONSUMER_GROUP = os.getenv('CONSUMER_GROUP')
MONGO_URI = os.getenv('MONGO_URI')