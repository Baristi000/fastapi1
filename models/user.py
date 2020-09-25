
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from db.base_class import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "user"
    id = Column(String(45), primary_key=True)
    user_name  = Column(String(45))  
    first_name = Column(String(45))  
    last_name = Column(String(45))    
    hashed_password = Column(String(200))  
    role = Column(String(45)) 
    last_login = Column(String(45))  
    activate = Column(String(45))  

class User_Account(BaseModel):
    username: str
    password: str

class NewUser(BaseModel):
    email: str
    role: str
