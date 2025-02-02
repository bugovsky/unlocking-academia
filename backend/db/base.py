from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from backend.db.config import DBSettings

Base = declarative_base()
db_settings = DBSettings()
engine = db_settings.engine
Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
