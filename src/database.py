from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.models import FileMetadataORM

# to pass sqlalchemy.exc.ArgumentError: Expected string or URL object, got MultiHostUrl
DATABASE_URL = str(settings.DATABASE_URL)
DATABASE_ASYNC_URL = str(settings.DATABASE_ASYNC_URL)

# Sync
# engine = create_engine(DATABASE_URL, echo=True)
# Session = sessionmaker(engine)
# # Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

# Async
engine = create_async_engine(url=DATABASE_ASYNC_URL, echo=True)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(FileMetadataORM.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(FileMetadataORM.metadata.drop_all)
