from dotenv import load_dotenv
import os

load_dotenv()

DATE_TIME_FORMAT = os.getenv("DATE_TIME_FORMAT", "%Y-%m-%d %H:%M:%S")
TAG_ADMIN = "admin 🦸‍♂️"

OLTP_USER = os.getenv("OLTP_USER")
OLTP_PASSWORD = os.getenv("OLTP_PASSWORD")
OLTP_HOST = os.getenv("OLTP_HOST")
OLTP_PORT = os.getenv("OLTP_PORT")
OLTP_DB = os.getenv("OLTP_DB")

USERS_DB_USER = os.getenv("USERS_DB_USER")
USERS_DB_PASSWORD = os.getenv("USERS_DB_PASSWORD")
USERS_DB_HOST = os.getenv("USERS_DB_HOST")
USERS_DB_PORT = os.getenv("USERS_DB_PORT")
USERS_DB_DB = os.getenv("USERS_DB_DB")

KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_TOPIC_LOCAL_DB_UPSERT_CATEGORY = os.getenv("KAFKA_TOPIC_LOCAL_DB_UPSERT_CATEGORY")
KAFKA_TOPIC_LOCAL_DB_UPSERT_PRODUCT = os.getenv("KAFKA_TOPIC_LOCAL_DB_UPSERT_PRODUCT")
KAFKA_TOPIC_LOCAL_DB_UPDATE_PRODUCT_DESC = os.getenv("KAFKA_TOPIC_LOCAL_DB_UPDATE_PRODUCT_DESC")

S3_PUBLIC_URL = os.getenv("S3_PUBLIC_URL")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")