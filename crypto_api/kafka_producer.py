from confluent_kafka import Producer
from crypto_api.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
import json

producer_config = {'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS}
producer = Producer(producer_config)

def send_message(key, value):
    try:
        serialized_value = json.dumps(value)
        producer.produce(KAFKA_TOPIC, key=key, value=serialized_value.encode('utf-8'))
        producer.flush()
    except Exception as e:
        print(f"Failed to send message to Kafka: {str(e)}")