"""
	Models for database
"""

from sqlalchemy import (
	Column, Integer,Text,
    String,DateTime, func,
    ForeignKey
)
from sqlalchemy.orm import declarative_base

from backend.schemas.post import PostConfig 

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(PostConfig.max_title_len), nullable=False)
    text = Column(String(PostConfig.max_text_len), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)
