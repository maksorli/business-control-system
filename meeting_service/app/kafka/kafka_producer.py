import json
from aiokafka import AIOKafkaProducer
import asyncio
from uuid import UUID
from datetime import datetime

producer = None

async def get_kafka_producer() -> AIOKafkaProducer:
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
        await producer.start()
    return producer

async def send_meeting_created_event(
    meeting_id: UUID,
    team_id: UUID,
    start_time: datetime,
    end_time: datetime,
    participant_ids: list[UUID]
):
    producer = await get_kafka_producer()
    data = {
        "meeting_id": str(meeting_id),
        "team_id": str(team_id),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "participant_ids": [str(uid) for uid in participant_ids]
    }
    await producer.send("meeting.created", json.dumps(data).encode())