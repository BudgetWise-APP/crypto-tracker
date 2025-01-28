from aiokafka import AIOKafkaConsumer
from bson import ObjectId
from .config import KAFKA_BOOTSTRAP_SERVERS
from common.mongo_client import db
import json

from integrations.services.binance_service import BinanceService
from integrations.services.bybit_service import BybitService


async def update_goal(user_id: str, platform: str, service, balance_method: str):
    goal = await db.goals.find_one({"user_id": ObjectId(user_id), "trackBy": platform})
    if goal:
        try:
            balance = await getattr(service, balance_method)(user_id)
            await db.goals.update_one(
                {"_id": goal["_id"]}, {"$set": {"currentStatus": balance}}
            )
        except Exception as e:
            print(f"Error updating {platform} goal for user {user_id}: {e}")
    else:
        print(f"No goal found for {platform} platform")


async def consume_messages(topic: str):
    try:
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id="crypto_integrations_group",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            key_deserializer=lambda k: k.decode("utf-8") if k else None
        )

        await consumer.start()
        print("Kafka Consumer started. Listening for messages...")
        try:
            async for msg in consumer:
                user_id = msg.value.get("user_id")
                try:
                    print("Updating goals")
                    await update_goal(
                        user_id, "binance", BinanceService, "get_total_balance_in_usd"
                    )
                    await update_goal(
                        user_id, "bybit", BybitService, "get_account_info"
                    )

                    print("Goals updated")
                except Exception as e:
                    print(f"Error processing message: {e}")
        finally:
            await consumer.stop()
            print("Kafka Consumer stopped")
    except Exception as e:
        print(f"Error consuming messages: {e}")
