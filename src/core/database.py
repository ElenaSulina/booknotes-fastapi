from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase

from core.config import config

db_uri = config.assemble_database_uri()
engine: AsyncEngine = create_async_engine(db_uri)


class Base(DeclarativeBase):
    pass


session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def create_async_session():
    session = session_factory()
    try:
        yield session
    finally:
        await session.close()
