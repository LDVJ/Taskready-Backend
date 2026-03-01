from sqlalchemy import create_engine
from .config import settings
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DB_URL= f'postgresql+psycopg://{settings.DB_USERNAME}:{settings.DB_PWD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}'

eng = create_engine(DB_URL)

ssession_local = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=eng
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = ssession_local()
    try:
        yield db
    finally:
        db.close()