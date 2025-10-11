"""
    Models for database
"""

from sqlalchemy import (
    Column, Integer,Text,
    String,DateTime, func,
    ForeignKey
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase 

class Base(AsyncAttrs ,DeclarativeBase):
    pass

class ModMessages(Base):
    __tablename__ = "messages_wait_mod"
    post_id = Column(String,primary_key=True)
    admin_id = Column(String, primary_key=True)
    message_id = Column(Integer, nullable=False)

