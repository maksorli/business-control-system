from aiokafka.admin import AIOKafkaAdminClient, NewTopic
import asyncio

TOPICS_TO_CREATE = [
    {"name": "meeting.created", "partitions": 1, "replication_factor": 1}
]

async def create_kafka_topics(retries=10, delay=3):
    for attempt in range(retries):
        try:
            admin = AIOKafkaAdminClient(bootstrap_servers="kafka:9092")
            await admin.start()
            break
        except Exception:
            print(f"[Kafka] Retry {attempt+1}/{retries} – waiting {delay}s...")
            await asyncio.sleep(delay)
    else:
        print("[Kafka] ❌ Could not connect")
        return

    try:
        existing = await admin.list_topics()
        to_create = [
            NewTopic(t["name"], t["partitions"], t["replication_factor"])
            for t in TOPICS_TO_CREATE if t["name"] not in existing
        ]
        if to_create:
            await admin.create_topics(to_create)
            print(f"[Kafka] Created: {[t.name for t in to_create]}")
    finally:
        await admin.close()
