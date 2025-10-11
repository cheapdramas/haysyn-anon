"""
	Utils for database usage
"""

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.engine import Engine 

from typing import AsyncGenerator

from .models import Base

from backend.core.config import DATABASE_URL





class DatabaseHelper:
    def __init__(self, url: str):
        self.engine: AsyncEngine = create_async_engine(url)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=True          
		)
        #TURNS ON FOREIGN KEYS CONSTRAINTS SQLITE3
        @event.listens_for(self.engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    async def db_init(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session 

db_helper = DatabaseHelper(DATABASE_URL)
