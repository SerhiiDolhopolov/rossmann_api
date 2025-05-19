from datetime import datetime, timezone

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

from app.config import KAFKA_HOST, KAFKA_PORT
from app.config import KAFKA_TOPIC_LOCAL_DB_UPSERT_CATEGORY, KAFKA_TOPIC_LOCAL_DB_UPSERT_PRODUCT
from rossmann_sync_schemas import CategorySchema, ProductSchema


producer = None


async def init_producer():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}',)
    await producer.start()

async def close_producer():
    await producer.stop()

async def send_with_reconnect(topic, payload, headers, key = None):
    global producer
    try:
        await producer.send_and_wait(topic, payload, headers=headers, key=key)
    except KafkaConnectionError:
        await close_producer()
        await init_producer()
        await producer.send_and_wait(topic, payload, headers=headers, key=key)
        
async def upsert_category_to_local_db(category_id: int, name: str, description: str | None, is_deleted: bool):
    category_sync_schema = CategorySchema(category_id=category_id, 
                                          name=name, 
                                          description=description, 
                                          is_deleted=is_deleted)
    updated_at_utc = datetime.now(timezone.utc)
    
    #For monkey patching at local db
    updated_at_utc = datetime(2025, 8, 5, 8, 0)
    topic = KAFKA_TOPIC_LOCAL_DB_UPSERT_CATEGORY
    payload = category_sync_schema.model_dump_json().encode()
    headers = [
        ('updated_at_utc', updated_at_utc.isoformat().encode()),
    ]
    await send_with_reconnect(topic, payload, headers=headers)
    
async def upsert_product_to_local_db(product_id: int, 
                                     name: str, 
                                     description: str | None, 
                                     barcode: str, 
                                     category_id: int, 
                                     price: float, 
                                     discount: float,
                                     is_deleted: bool):
    product_sync_schema = ProductSchema(product_id=product_id,
                                        name=name,
                                        description=description,
                                        barcode=barcode,
                                        category_id=category_id,
                                        price=price,
                                        discount=discount,
                                        is_deleted=is_deleted)
    updated_at_utc = datetime.now(timezone.utc)
    
    #For monkey patching at local db
    updated_at_utc = datetime(2025, 8, 5, 8, 0)
    topic = KAFKA_TOPIC_LOCAL_DB_UPSERT_PRODUCT
    payload = product_sync_schema.model_dump_json().encode()
    headers = [
        ('updated_at_utc', updated_at_utc.isoformat().encode()),
    ]
    await send_with_reconnect(topic, payload, headers=headers)
