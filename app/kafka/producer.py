from datetime import datetime, timezone

from aiokafka import AIOKafkaProducer

from app.config import KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC_LOCAL_DB_UPSERT_CATEGORY
from rossmann_sync_schemas import CategorySchema


producer = None


async def init_producer():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}',)
    await producer.start()

async def close_producer():
    await producer.stop()
    
async def upsert_category_to_local_db(category_id: int, name: str, description: str | None, is_deleted: bool):
    category_sync_schema = CategorySchema(category_id=category_id, 
                                          name=name, 
                                          description=description, 
                                          is_deleted=is_deleted)
    updated_at_utc = datetime.now(timezone.utc)
    updated_at_utc = datetime(2025, 8, 5, 8, 0)
    topic = KAFKA_TOPIC_LOCAL_DB_UPSERT_CATEGORY
    payload = category_sync_schema.model_dump_json().encode()
    headers = [
        ('updated_at_utc', updated_at_utc.isoformat().encode()),
    ]
    await producer.send_and_wait(topic, payload, headers=headers, key=payload)
