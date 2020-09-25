
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from db.base_class import Base

class Channel_Manager(Base):
    __tablename__ = "channel_manager"
    channel_id = Column(String(45), primary_key=True)
    manager_id  = Column(String(45), primary_key=True)
