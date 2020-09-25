from sqlalchemy.orm import Session
from sqlalchemy import update
from models import shop
from crud import crud_shop_executor,crud_channel_manager,crud_shop,crud_channel,crud_country
from schemas import shop_schema

def get_shop(db: Session, shop_id: int):
    return db.query(shop.Shop).filter(shop.Shop.id == shop_id).first()

def get_all_shops(db: Session, skip: int = 0, limit: int = 100):
    shops=db.query(shop.Shop).offset(skip).limit(limit).all()
    for s in shops:
        s.channel_name=crud_channel.get_channel(db=db,channel_id=s.channel_id).name
        s.country_name=crud_country.get_country(db=db,country_id=s.postal_code).name
    return shops
def update_shop_sim(db:Session,sim_number:str,shop_id:str):
    db.query(shop.Shop).filter(shop.Shop.id == shop_id).update({shop.Shop.sim_number:sim_number})
    db.commit()

def create_shop(db: Session, created_shop: shop_schema.ShopCreate):
    db_shop = shop.Shop(id=created_shop.id,name=created_shop.name, postal_code=created_shop.postal_code,
    channel_id=created_shop.channel_id,correspond_apicall=created_shop.correspond_apicall)
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

def count_shop(db:Session,channel_id:str):
    return db.query(shop.Shop).filter(shop.Shop.channel_id == channel_id).count()

def count_shop_country(db:Session,postal_code:str):
    return db.query(shop.Shop).filter(shop.Shop.postal_code == postal_code).count()


def get_all_shop_of_executor(db:Session,executor_id:str):
    all_shop_id=[]
    for id in crud_shop_executor.get_shop_id_of_executor(db=db,executor_id=executor_id):
        all_shop_id.append(id[0])
    shops=db.query(shop.Shop).filter(shop.Shop.id.in_(all_shop_id)).all()
    for s in shops:
        s.channel_name=crud_channel.get_channel(db=db,channel_id=s.channel_id).name
        s.country_name=crud_country.get_country(db=db,country_id=s.postal_code).name
    return shops


def get_all_not_shop_of_executor(db:Session,executor_id:str):
    all_shop_id=[]
    for id in crud_shop_executor.get_shop_id_of_executor(db=db,executor_id=executor_id):
        all_shop_id.append(id[0])

    return db.query(shop.Shop).filter(shop.Shop.id.notin_(all_shop_id)).all()

def get_all_shop_of_manager(db:Session,manager_id:str):
    all_channel_id=[]
    for id in crud_channel_manager.get_channel_id_of_manager(db=db,manager_id=manager_id):
        all_channel_id.append(id[0])

    return db.query(shop.Shop).filter(shop.Shop.channel_id.in_(all_channel_id)).all()

def check_shop_manager(db:Session,shop_id:str,manager_id:str):
    current_shop=crud_shop.get_shop(db=db,shop_id=shop_id)
    if crud_channel_manager.get_channel_manager(db=db,channel_id=current_shop.channel_id,manager_id=manager_id) is None:
        return True
    return False

def get_all_shop_channel(db:Session,channel_id:str):
    shops= db.query(shop.Shop).filter(shop.Shop.channel_id==channel_id).all()
    for s in shops:
        s.channel_name=crud_channel.get_channel(db=db,channel_id=s.channel_id).name
        s.country_name=crud_country.get_country(db=db,country_id=s.postal_code).name
    return shops

def get_all_shop_country(db:Session,postal_code:str):
    return db.query(shop.Shop).filter(shop.Shop.postal_code==postal_code).all()