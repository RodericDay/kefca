from fastapi import FastAPI
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json


app = FastAPI()

KAFKA_TOPIC = "fastapi-demo"
KAFKA_BROKER = "kafka:9092"

# Kafka Producer
async def get_kafka_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()
    return producer

# Kafka Consumer (Background Task)
async def consume_messages():
    await asyncio.sleep(3)
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    print('Starting...')
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Consumed message: {msg.value}")  # Just print messages for now
    finally:
        print('Stopped.')
        await consumer.stop()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_messages())  # Start consumer in the background

@app.post("/send/")
async def send_message(message: str):
    producer = await get_kafka_producer()
    await producer.send(KAFKA_TOPIC, {"message": message})
    await producer.stop()
    return {"status": "Message sent!", "message": message}
