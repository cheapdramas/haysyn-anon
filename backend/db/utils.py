"""
	Utils for database usage
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base 

DATABASE_URL = "sqlite:///./db.sqlite3"

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
