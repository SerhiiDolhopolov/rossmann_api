from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

OLTP_USER = os.getenv("OLTP_USER")
OLTP_PASSWORD = os.getenv("OLTP_PASSWORD")
OLTP_HOST = os.getenv("OLTP_HOST")
OLTP_PORT = os.getenv("OLTP_PORT")
OLTP_DB = os.getenv("OLTP_DB")

DATABASE_URL = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}".format(
    username=OLTP_USER,
    password=OLTP_PASSWORD,
    dbname=OLTP_DB,
    host=OLTP_HOST,
    port=OLTP_PORT,
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    