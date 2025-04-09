import json
import asyncio
from uuid import UUID
from datetime import datetime, timedelta

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from app.core.database import AsyncSessionLocal
from app.repositories.calendar_repository import CalendarRepository
from app.schemas.calendar_event import CalendarEventCreate

TOPICS = ["task.created", "meeting.created"]
BOOTSTRAP_SERVERS = "kafka:9092"
GROUP_ID = "calendar-service"


async def consume_events():
    consumer = None

    for attempt in range(10):
        try:
            consumer = AIOKafkaConsumer(
                *TOPICS,
                bootstrap_servers=BOOTSTRAP_SERVERS,
                group_id=GROUP_ID,
            )
            await consumer.start()
            print("[Kafka] ✅ Consumer connected")
            break
        except KafkaConnectionError:
            print(f"[Kafka] 🔄 Attempt {attempt + 1}/10 - waiting 10s...")
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
            try:
                data = json.loads(msg.value.decode())
            except json.JSONDecodeError:
                print("[Kafka] ❌ Invalid JSON, skipping...")
                continue

            async with AsyncSessionLocal() as session:
                repo = CalendarRepository(session)

                if msg.topic == "meeting.created":
                    try:
                        for user_id in data["participant_ids"]:
                            event = CalendarEventCreate(
                                title="Meeting",
                                start_time=datetime.fromisoformat(data["start_time"]),
                                end_time=datetime.fromisoformat(data["start_time"]) + timedelta(hours=1),
                                type="meeting",
                                related_id=UUID(data["meeting_id"]),
                                user_id=UUID(user_id),
                            )
                            await repo.create(event)
                    except Exception as e:
                        print(f"[Kafka] ❌ Error handling meeting.created: {e}")

                elif msg.topic == "task.created":
                    try:
                        event = CalendarEventCreate(**data)
                        await repo.create(event)
                    except Exception as e:
                        print(f"[Kafka] ❌ Error handling task.created: {e}")
    finally:
        if consumer:
            await consumer.stop()
            print("[Kafka] 🔌 Consumer closed")
