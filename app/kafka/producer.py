from datetime import datetime, timezone
import logging
import asyncio

from fastapi import Request
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError
from rossmann_sync_schemas import CategorySchema, ProductSchema, ProductDescSchema

from app.config import (
    KAFKA_HOST,
    KAFKA_PORT,
    KAFKA_TOPIC_LOCAL_DB_UPSERT_CATEGORY,
    KAFKA_TOPIC_LOCAL_DB_UPSERT_PRODUCT,
    KAFKA_TOPIC_LOCAL_DB_UPDATE_PRODUCT_DESC,
)

logger = logging.getLogger(__name__)



def get_kafka_producer(request: Request) -> AIOKafkaProducer:
    return request.app.state.kafka_producer


async def init_producer() -> AIOKafkaProducer:
    producer = AIOKafkaProducer(bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}")
    await producer.start()
    return producer


async def close_producer(producer: AIOKafkaProducer):
    await producer.stop()


async def send_with_reconnect(
    producer: AIOKafkaProducer,
    topic,
    payload,
    headers=None,
    key=None,
    max_retries: int = 3,
    retry_delay: float = 2.0,
) -> AIOKafkaProducer:
    if not headers:
        headers = []
    attempt = 0
    while attempt < max_retries:
        try:
            await producer.send_and_wait(
                topic,
                payload,
                headers=headers,
                key=key,
            )
            return producer
        except KafkaConnectionError as e:
            logger.warning(
                "Kafka connection error: %s, reconnecting... (attempt %s)",
                e,
                attempt + 1,
            )
            await close_producer(producer)
            producer = await init_producer()
        except Exception as e:
            logger.error(
                "Unexpected error while sending to Kafka: %s (attempt %s)",
                e,
                attempt + 1,
                exc_info=True,
            )
            if attempt == max_retries - 1:
                raise
        attempt += 1
        await asyncio.sleep(retry_delay)
    return producer


async def upsert_category_to_local_db(
    producer: AIOKafkaProducer,
    category_id: int,
    name: str,
    description: str | None,
    is_deleted: bool,
) -> AIOKafkaProducer:
    updated_at_utc = datetime.now(timezone.utc)
    category_sync_schema = CategorySchema(
        category_id=category_id,
        name=name,
        description=description,
        is_deleted=is_deleted,
        updated_at_utc=updated_at_utc,
    )
    topic = KAFKA_TOPIC_LOCAL_DB_UPSERT_CATEGORY
    payload = category_sync_schema.model_dump_json().encode()
    producer = await send_with_reconnect(producer, topic, payload)
    return producer


async def upsert_product_to_local_db(
    producer: AIOKafkaProducer,
    product_id: int,
    name: str,
    description: str | None,
    barcode: str,
    category_id: int,
    price: float,
    discount: float,
    is_deleted: bool,
) -> AIOKafkaProducer:
    updated_at_utc = datetime.now(timezone.utc)
    product_sync_schema = ProductSchema(
        product_id=product_id,
        name=name,
        description=description,
        barcode=barcode,
        category_id=category_id,
        price=price,
        discount=discount,
        is_deleted=is_deleted,
        updated_at_utc=updated_at_utc,
    )
    topic = KAFKA_TOPIC_LOCAL_DB_UPSERT_PRODUCT
    payload = product_sync_schema.model_dump_json().encode()
    producer = await send_with_reconnect(producer, topic, payload)
    return producer


async def update_product_desc_to_local_db(
    producer: AIOKafkaProducer,
    product_id: int,
    name: str,
    description: str | None,
    barcode: str,
    category_id: int,
    is_deleted: bool,
) -> AIOKafkaProducer:
    updated_at_utc = datetime.now(timezone.utc)
    product_desc_sync_schema = ProductDescSchema(
        product_id=product_id,
        name=name,
        description=description,
        barcode=barcode,
        category_id=category_id,
        is_deleted=is_deleted,
        updated_at_utc=updated_at_utc,
    )
    topic = KAFKA_TOPIC_LOCAL_DB_UPDATE_PRODUCT_DESC
    payload = product_desc_sync_schema.model_dump_json().encode()
    producer = await send_with_reconnect(producer, topic, payload)
    return producer