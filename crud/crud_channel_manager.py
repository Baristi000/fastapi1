from sqlalchemy.orm import Session

from models import channel_manager
from schemas import channel_manager_schema

def get_channel_manager(db: Session, channel_id: str,manager_id:str):
    return db.query(channel_manager.Channel_Manager).filter(channel_manager.Channel_Manager.channel_id == channel_id,channel_manager.Channel_Manager.manager_id == manager_id).first()

def create_channel_manager(db: Session, manager_id:str,channel_id:str):
    db_channel_manager= channel_manager.Channel_Manager(channel_id=channel_id,manager_id=manager_id)
    db.add(db_channel_manager)
    db.commit()
    db.refresh(db_channel_manager)
    return db_channel_manager

def count_manager_of_channel(db:Session,channel_id:str):
    return db.query(channel_manager.Channel_Manager).filter(channel_manager.Channel_Manager.channel_id == channel_id).count()

def count_channel_manager(db:Session,manager_id:str):
    return db.query(channel_manager.Channel_Manager).filter(channel_manager.Channel_Manager.manager_id == manager_id).count()

def get_manager_id_of_channel(db:Session,channel_id:str):
    return db.query(channel_manager.Channel_Manager.manager_id).filter(channel_manager.Channel_Manager.channel_id == channel_id).all()

def get_channel_id_of_manager(db:Session,manager_id:str):
    return db.query(channel_manager.Channel_Manager.channel_id).filter(channel_manager.Channel_Manager.manager_id == manager_id).all()

def delete_channel_manager(db: Session,channel_id:str,manager_id:str):
    db_channel_manager =db.query(channel_manager.Channel_Manager).filter(channel_manager.Channel_Manager.channel_id == channel_id,channel_manager.Channel_Manager.manager_id == manager_id).first()
    db.delete(db_channel_manager)
    db.commit()
    return {"message":"delete success"}

