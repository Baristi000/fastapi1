from sqlalchemy.orm import Session
from api import deps
from fastapi import APIRouter, Depends, HTTPException,status
from models import country
from crud import crud_shop
from schemas import country_schema

def get_country(db: Session, country_id: str):
    return db.query(country.Country).filter(country.Country.postl_code == country_id).first()

def get_all_country(db: Session):
    countries=db.query(country.Country).all()
    for s in countries:
        s.count_shop=crud_shop.count_shop_country(db=db,postal_code=s.postl_code)
    return countries




