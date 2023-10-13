"""Contains the database engine and sessionmaker."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from common.settings import settings

engine = create_async_engine(str(settings.database_url))
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
