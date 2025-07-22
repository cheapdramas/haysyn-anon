"""
	Models for database
"""

from sqlalchemy import (
	Column, Integer,
	Text, String,
    DateTime, func
)
from sqlalchemy.orm import declarative_base

from config import PostConfig


Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(PostConfig.max_title_len), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
