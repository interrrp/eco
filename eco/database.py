from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from eco.settings import settings

engine = create_async_engine(settings.sqlite_url)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
