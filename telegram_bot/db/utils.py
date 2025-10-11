"""
	Utils for database usage
"""
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from .models import Base
from typing import AsyncGenerator
from core.config import DATABASE_URL


class DatabaseHelper:
    def __init__(self, url: str):
        self.engine: AsyncEngine = create_async_engine(url)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=True          
		)
    async def db_init(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session 

db_helper = DatabaseHelper(DATABASE_URL)
