
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from db.base_class import Base

class Shop(Base):
    __tablename__ = "shop"
    id = Column(String(45), primary_key=True)
    name = Column(String(45))  
    postal_code = Column(String(45))  
    sim_number = Column(String(45))  
    channel_id = Column(String(45))  
    correspond_apicall = Column(String(200))   

