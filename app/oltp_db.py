from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import (
    OLTP_USER,
    OLTP_PASSWORD,
    OLTP_HOST,
    OLTP_PORT,
    OLTP_DB,
)

DATABASE_URL = (
    f"postgresql+psycopg2://{OLTP_USER}:{OLTP_PASSWORD}@"
    f"{OLTP_HOST}:{OLTP_PORT}/{OLTP_DB}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
