
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from db.base_class import Base

class Message(Base):
    __tablename__ = "message"
    phone_owner = Column(String(45))
    time = Column(String(45), primary_key=True) 
    otp = Column(String(45), primary_key=True)  
    raw_message = Column(String(200))  
    from_number = Column(String(45))  
    date= Column(String(45)) 
    shop_id = Column(String(45))   
  

