"""SQLAlchemy database setup, session management, and base models."""

from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from ams_common.config import ServiceSettings
from ams_common.logging import get_logger

_LOG = get_logger(__name__)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all models."""
    pass


def get_sync_engine(settings: ServiceSettings):
    """Synchronous engine (for Alembic migrations)."""
    return create_engine(
        settings.db_url,
        echo=settings.db_echo,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
    )


def get_async_engine(settings: ServiceSettings):
    """Asynchronous engine (for FastAPI services)."""
    # Convert postgresql+psycopg2://... to postgresql+asyncpg://...
    async_url = settings.db_url.replace("psycopg2", "asyncpg")
    return create_async_engine(
        async_url,
        echo=settings.db_echo,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
    )


def get_sync_session_factory(settings: ServiceSettings):
    """Synchronous session factory (for Alembic)."""
    engine = get_sync_engine(settings)
    return sessionmaker(engine, class_=Session, expire_on_commit=False)


def get_async_session_factory(settings: ServiceSettings):
    """Asynchronous session factory (for FastAPI)."""
    engine = get_async_engine(settings)
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session(
    settings: ServiceSettings,
) -> AsyncGenerator[AsyncSession, None]:
    """Async session generator for dependency injection in FastAPI."""
    factory = get_async_session_factory(settings)
    async with factory() as session:
        yield session
