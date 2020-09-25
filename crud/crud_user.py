from sqlalchemy.orm import Session
from sqlalchemy import and_
from api import deps
from models import user
from schemas import user_schema
from crud import crud_channel_manager,crud_shop_executor
import random
from fastapi import APIRouter, Depends, HTTPException
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_user(db: Session, user_id: str):
    return db.query(user.User).filter(user.User.id == user_id).first()

def get_all_executor(db:Session):
    executors=db.query(user.User).filter(user.User.role=="executor").all()
    for executor in executors:
        executor.shop_count=crud_shop_executor.count_executors_shop(db=db,executor_id=executor.id)
    return executors

def get_all_manager(db:Session):
    managers=db.query(user.User).filter(user.User.role=="manager").all()
    for manager in managers:
        manager.channel_count=crud_channel_manager.count_channel_manager(db=db,manager_id=manager.id)
    return managers

def get_all_user(db: Session):
    return db.query(user.User).all()

def get_user_by_username(db: Session, user_name: str):
    user_db=db.query(user.User).filter(user.User.user_name == user_name).first()
    return user_db
def create_user(db: Session, users: user_schema.UserCreate):
    db_user = user.User(id=users.id,user_name=users.user_name, role=users.role,activate="1")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_channel_manager(db:Session,channel_id:str):
    manager_id=crud_channel_manager.get_manager_id_of_channel(db=db,channel_id=channel_id)
    all_manager_id=[]
    for id in manager_id:
        all_manager_id.append(id[0])

    return db.query(user.User).filter(user.User.id.in_(all_manager_id)).all()

def get_all_shop_executors(db:Session,shop_id:str):
    executor_id=crud_shop_executor.get_executor_id_of_shop(db=db,shop_id=shop_id)
    all_executor_id=[]
    for id in executor_id:
        all_executor_id.append(id[0])

    return db.query(user.User).filter(user.User.id.in_(all_executor_id)).all()

def get_all_manager_not_belong_to_channel(db:Session,channel_id:str):
    manager_id=crud_channel_manager.get_manager_id_of_channel(db=db,channel_id=channel_id)
    all_manager_id=[]
    for id in manager_id:
        all_manager_id.append(id[0])

    return db.query(user.User).filter(and_(user.User.id.notin_(all_manager_id),user.User.role=="manager")).all()

def get_all_shop_not_belong_to_executors(db:Session,shop_id:str):
    executor_id=crud_shop_executor.get_executor_id_of_shop(db=db,shop_id=shop_id)
    all_executor_id=[]
    for id in executor_id:
        all_executor_id.append(id[0])

    return db.query(user.User).filter(and_(user.User.id.notin_(all_executor_id),user.User.role=="executor")).all()

def inactivate_user(db:Session,user_id:str,activate:str):
    db.query(user.User).filter(user.User.id == user_id).update({user.User.activate:activate})
    db.commit()

def create_new_user(db:Session,user_name:str,role:str):
    db_user = user.User(id=get_random_string(8),user_name=user_name, role=role,activate="1")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user