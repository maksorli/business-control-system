import json
from aiokafka import AIOKafkaConsumer
from app.repositories.calendar_repository import CalendarRepository
from app.schemas.calendar_event import CalendarEventCreate
from app.core.database import AsyncSessionLocal
from aiokafka.errors import KafkaConnectionError
import asyncio

async def consume_events():
    consumer = None

    for attempt in range(10):
        try:
            consumer = AIOKafkaConsumer(
                "task.created", "meeting.created",
                bootstrap_servers="kafka:9092",
                group_id="calendar-service"
            )
            await consumer.start()
            print("[Kafka] 🟢 Consumer connected")
            break
        except KafkaConnectionError:
            print(f"[Kafka] 🔄 Attempt {attempt+1}/10 - waiting 10s...")
            await asyncio.sleep(10)
        except Exception as e:
            print(f"[Kafka] ❌ Unexpected error: {e}")
            await asyncio.sleep(10)
    else:
        print("[Kafka] ❌ Could not connect after retries")
        return

    try:
        async for msg in consumer:
            print(f"[Kafka] 📥 {msg.topic}: {msg.value}")
            data = json.loads(msg.value.decode())
            async with AsyncSessionLocal() as session:
                repo = CalendarRepository(session)
                await repo.create(CalendarEventCreate(**data))
    finally:
        if consumer:
            await consumer.stop()
            print("[Kafka] 🔌 Consumer closed")