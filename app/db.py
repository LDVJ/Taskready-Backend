from sqlalchemy import create_engine
from .config import DB_Setting
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DB_URL= f'postgresql+psycopg://{DB_Setting.DB_USERNAME}:{DB_Setting.DB_PWD}@{DB_Setting.DB_HOSTNAME}:{DB_Setting.DB_PORT}/{DB_Setting.DB_NAME}'

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