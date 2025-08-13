"""
	Utils for database usage
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine 

from .models import Base

from backend.config import DATABASE_URL


#TURNS ON FOREIGN KEYS CONSTRAINTS SQLITE3
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class DatabaseHelper:
    def __init__(self, url: str):
        self.engine = create_engine(url, connect_args={"check_same_thread": False})
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=True          
		)
    def db_init(self) -> None:
        Base.metadata.create_all(bind=self.engine)
    def session_getter(self) -> Session:
        with self.session_factory() as session:
            yield session 

db_helper = DatabaseHelper(DATABASE_URL)
