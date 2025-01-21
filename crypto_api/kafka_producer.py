from confluent_kafka import Producer
from common.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer_config = {'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS}
producer = Producer(producer_config)


def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def send_message(key, value):
    try:
        serialized_value = json.dumps(value)
        producer.produce(
            KAFKA_TOPIC,
            key=key,
            value=serialized_value.encode('utf-8'),
            callback=delivery_report,
        )
        producer.flush()
        logger.info(f"Message sent to Kafka: {serialized_value}")
    except Exception as e:
        print(f"Failed to send message to Kafka: {str(e)}")
