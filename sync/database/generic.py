from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from setting.config import get_settings
from models.users import User
from models.item import Item


settings = get_settings()


engine = create_engine(
    settings.database_url ,
    echo=True,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    return SessionLocal()

def init_db():
    Base.metadata.create_all(bind=engine, tables=[User.__table__, Item.__table__])