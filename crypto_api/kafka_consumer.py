from confluent_kafka import Consumer, KafkaException
from common.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, CONSUMER_GROUP

consumer_config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': CONSUMER_GROUP,
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(consumer_config)
consumer.subscribe([KAFKA_TOPIC])


def consume_messages():
    try:
        while True:
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaException(message.error()):
                    continue
                else:
                    raise KafkaException(message.error())
            print(f"Consumed message: {message.value().decode('utf-8')}")
    except Exception as e:
        print(f"Failed to consume message: {str(e)}")
    finally:
        consumer.close()
