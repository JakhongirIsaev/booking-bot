"""
Async database session management.

Provides:
- async engine creation
- async session factory
- get_session() async context manager for dependency injection
- init_db() to create all tables (used in development / MVP)
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import settings
from app.database.base import Base

# Create async engine
# echo=False in production, set True for SQL debugging
engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=10,
    max_overflow=20,
)

# Session factory — produces AsyncSession instances
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager that yields a database session.

    Usage:
        async with get_session() as session:
            result = await session.execute(...)
    """
    session = async_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def init_db() -> None:
    """
    Create all database tables.

    Used for MVP / development. In production, use Alembic migrations.
    """
    # Import all models so Base.metadata knows about them
    import app.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Dispose the database engine on shutdown."""
    await engine.dispose()
