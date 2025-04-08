from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import KafkaConnectionError
import asyncio
from app.kafka.config import TOPICS_TO_CREATE

async def create_kafka_topics(retries: int = 10, delay: int = 3):
    for attempt in range(retries):
        try:
            admin = AIOKafkaAdminClient(bootstrap_servers="kafka:9092")
            await admin.start()
            print("[Kafka] Admin client connected ✅")
            break
        except KafkaConnectionError:
            print(f"[Kafka] Attempt {attempt+1}/{retries} - broker not ready, retrying in {delay}s...")
            await asyncio.sleep(delay)
    else:
        print("[Kafka] ❌ Could not connect to Kafka after retries")
        return

    try:
        existing_topics = await admin.list_topics()
        to_create = [
            NewTopic(t["name"], num_partitions=t["partitions"], replication_factor=t["replication_factor"])
            for t in TOPICS_TO_CREATE if t["name"] not in existing_topics
        ]
        if to_create:
            await admin.create_topics(to_create)
            print(f"[Kafka] Created topics: {[t.name for t in to_create]}")
        else:
            print("[Kafka] All topics already exist")
    finally:
        await admin.close()
