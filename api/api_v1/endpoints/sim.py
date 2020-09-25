from typing import Any, List,Optional

from fastapi import APIRouter, Depends, HTTPException,Header,status
from sqlalchemy.orm import Session
from core.config import settings
import crud, models, schemas
from crud import crud_sim
from schemas import sim_schema,message_schema
from api import deps
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
import mysql.connector
router = APIRouter()

def check_sercurity_scopes(token,scopes):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    role: str = payload.get("role")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    if role=="executor":
        if not (scopes in settings.EXECUTOR_SCOPES):
            raise  credentials_exception
    elif role=="manager":
        if not (scopes in settings.MANAGER_SCOPES):
            raise  credentials_exception
    elif role=="newuser":
        if not (scopes in settings.NEWUSER_SCOPES):
            raise  credentials_exception
    return payload.get("id")
    


    
@router.get("/{sim_number}")
def get_sim_db(sim_number:str,token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_SIM_DETAIL_SCOPE)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (mysql.connector.Error):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="My sql connection error ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return crud_sim.get_sim_by_number(db=db,sim_number=sim_number)
@router.get("/")
def get_all_sim(token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_SIM_DETAIL_SCOPE)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (mysql.connector.Error):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="My sql connection error ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return crud_sim.get_all_sim(db=db)

@router.get("/{sim_number}/all-messages")
def get_sim_db(sim_number:str,token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_SIM_DETAIL_SCOPE)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (mysql.connector.Error):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="My sql connection error ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return crud_sim.get_message(db=db,sim_number=sim_number)

@router.get("/{sim_number}/shop-count")
def get_sim_db(sim_number:str,token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_SIM_DETAIL_SCOPE)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (mysql.connector.Error):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="My sql connection error ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return crud_sim.count_shop(db=db,sim_number=sim_number)