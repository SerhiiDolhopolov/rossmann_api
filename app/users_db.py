from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import USERS_DB_USER, USERS_DB_PASSWORD, USERS_DB_DB, USERS_DB_HOST, USERS_DB_PORT


DATABASE_URL = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}".format(
    username=USERS_DB_USER,
    password=USERS_DB_PASSWORD,
    dbname=USERS_DB_DB,
    host=USERS_DB_HOST,
    port=USERS_DB_PORT,
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    