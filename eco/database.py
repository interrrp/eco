from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from eco.settings import settings

engine = create_async_engine(settings.sqlite_url)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
