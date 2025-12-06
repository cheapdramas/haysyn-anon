"""
	Models for database
"""

from sqlalchemy import (
	Column, Integer,Text,
    String,DateTime, func,
    ForeignKey, CheckConstraint, Boolean
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase 


from backend.schemas.post import MAX_TITLE_LEN, MAX_TEXT_LEN

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(MAX_TITLE_LEN), nullable=False)
    text = Column(String(MAX_TEXT_LEN), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    telegram_user_id = Column(String(64), nullable=True)
    in_tg_channel = Column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint(likes >= 0, name='check_positive_value'),
        CheckConstraint(dislikes >= 0, name='check_positive_value'),
    )

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)
