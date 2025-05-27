from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import (
    USERS_DB_USER,
    USERS_DB_PASSWORD,
    USERS_DB_DB,
    USERS_DB_HOST,
    USERS_DB_PORT,
)

DATABASE_URL = (
    f"postgresql+psycopg2://{USERS_DB_USER}:{USERS_DB_PASSWORD}@"
    f"{USERS_DB_HOST}:{USERS_DB_PORT}/{USERS_DB_DB}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
