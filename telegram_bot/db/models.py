"""
    Models for database
"""

from sqlalchemy import (
    Column, Integer,Text,
    String,DateTime, func,
    ForeignKey
)
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class ModMessages(Base):
    __tablename__ = "messages_wait_mod"
    post_id = Column(String,primary_key=True)
    admin_id = Column(String, primary_key=True)
    message_id = Column(Integer, nullable=False)

