from sqlalchemy.orm import Session

from models import shop_executor
from schemas import shop_executor_schema

def get_shop_executor(db: Session, shop_id: str,executor_id:str):
    return db.query(shop_executor.Shop_Executor).filter(shop_executor.Shop_Executor.shop_id == shop_id,shop_executor.Shop_Executor.executor_id == executor_id).first()

def create_shop_executor(db: Session, created_shop_executor: shop_executor_schema.Shop_ExecutorCreate):
    db_shop_executor = shop_executor.Shop_Executor(shop_id=created_shop_executor.shop_id,executor_id=created_shop_executor.executor_id)
    db.add(db_shop_executor)
    db.commit()
    db.refresh(db_shop_executor)
    return db_shop_executor

def create_new_shop_executor(db: Session, shop_id:str,executor_id:str):
    db_shop_executor = shop_executor.Shop_Executor(shop_id=shop_id,executor_id=executor_id)
    db.add(db_shop_executor)
    db.commit()
    db.refresh(db_shop_executor)
    return db_shop_executor


def delete_shop_executor(db: Session,shop_id:str,executor_id:str):
    db_shop_executor =db.query(shop_executor.Shop_Executor).filter(shop_executor.Shop_Executor.shop_id ==shop_id,shop_executor.Shop_Executor.executor_id == executor_id).first()
    db.delete(db_shop_executor)
    db.commit()
    return {"message":"delete success"}

def count_shop_of_executors(db:Session,shop_id:str):
    return db.query(shop_executor.Shop_Executor).filter(shop_executor.Shop_Executor.shop_id == shop_id).count()

def count_executors_shop(db:Session,executor_id:str):
    return db.query(shop_executor.Shop_Executor).filter(shop_executor.Shop_Executor.executor_id == executor_id).count()


def get_executor_id_of_shop(db:Session,shop_id:str):
    return db.query(shop_executor.Shop_Executor.executor_id).filter(shop_executor.Shop_Executor.shop_id == shop_id).all()

def get_shop_id_of_executor(db:Session,executor_id:str):
    return db.query(shop_executor.Shop_Executor.shop_id).filter(shop_executor.Shop_Executor.executor_id == executor_id).all()
