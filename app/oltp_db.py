from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import OLTP_USER, OLTP_PASSWORD, OLTP_HOST, OLTP_PORT, OLTP_DB


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
    