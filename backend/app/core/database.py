"""Database configuration and session factory (async SQLAlchemy)."""

from __future__ import annotations

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from .config import Settings


settings = Settings()

# Async engine
engine = create_async_engine(settings.database_url, echo=False, future=True)

# Async session factory using async_sessionmaker (recommended for SQLAlchemy 2.0+)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
