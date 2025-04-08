import json
from aiokafka import AIOKafkaProducer

producer: AIOKafkaProducer | None = None

async def get_producer() -> AIOKafkaProducer:
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
        await producer.start()
    return producer

async def publish_event(topic: str, payload: dict):
    kafka = await get_producer()
    await kafka.send_and_wait(topic, json.dumps(payload).encode("utf-8"))
