from sqlalchemy import (
    Column, Integer,
    String
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class Base(AsyncAttrs ,DeclarativeBase):
    pass

class ModMessage(Base):
    __tablename__ = "messages_wait_mod"
    post_id = Column(String,primary_key=True)
    admin_id = Column(String, primary_key=True)
    message_id = Column(Integer, nullable=False)

class ChanellMessages(Base):
    __tablename__ = "channel_messages"
    user_id = Column(String(64), nullable=True)
    message_id = Column(Integer, nullable=False,primary_key=True)
    post_id = Column(String, nullable=True, unique=True)
