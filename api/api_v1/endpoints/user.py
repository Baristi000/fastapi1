from typing import Any, List,Optional
from core.config import settings
from fastapi import APIRouter, Depends, HTTPException,status,Header
from sqlalchemy.orm import Session
import json
import crud, models, schemas
from crud import crud_user,crud_shop,crud_channel,crud_shop_executor,crud_channel_manager
from schemas import user_schema,shop_schema,channel_schema
from api import deps
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from core import sercurity
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


@router.get("/", response_model=List[user_schema.User])
def All_users(token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    '''
    View All User
    '''
    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_ALL_USER_SCOPE)
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
    return crud_user.get_all_user(db=db)


@router.get("/executors")
def All_executors(token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    '''
    View All executor User
    '''
    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_ALL_USER_SCOPE)
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
    return crud_user.get_all_executor(db=db)

@router.get("/managers")
def All_managers(token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    '''
    View All manager User
    '''
    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_ALL_USER_SCOPE)
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
    return crud_user.get_all_manager(db=db)

@router.get("/create-user")
def All_users(user_name:str,role:str,token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    '''
    View All manager User
    '''
    try:
        check_sercurity_scopes(token=token,scopes=settings.ADD_NEW_USER)
        
        if not crud_user.get_user_by_username(db=db,user_name=user_name) is None:
            raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="User already exist "
        )
        if sercurity.check_email(user_name) is False:
            raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid user name "
        )
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
    return {"message":"success"}

@router.get("/{id}", response_model=user_schema.User)
def user_detail(id:str,token:Optional[str] = Header(None), db: Session = Depends(deps.get_db)):
    '''
    View user detail  with user id 
    '''
    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_USER_DETAIL_SCOPE)
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
    return crud_user.get_user(db=db,user_id=id)

@router.post("/{id}/inactivate")
def Inactivate_user(id:str,token:Optional[str] = Header(None), db: Session = Depends(deps.get_db)):
    '''
    Inactivate user
    '''
    try:
        check_sercurity_scopes(token=token,scopes=settings.INACTIVATE_USER_SCOPE)
        crud_user.inactivate_user(db=db,user_id=id,activate="0")
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
    return {"message":"Inactivate success"}

@router.post("/{id}/activate")
def get_dbuser(id:str,token:Optional[str] = Header(None), db: Session = Depends(deps.get_db)):
    '''
    Activate user
    '''
    try:
        check_sercurity_scopes(token=token,scopes=settings.INACTIVATE_USER_SCOPE)
        crud_user.inactivate_user(db=db,user_id=id,activate="1")
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
    return {"message":"Activate success"}

@router.get("/{executor_id}/all-shop")
def get_all_shops_executor(executor_id:str,token:Optional[str] = Header(None), db: Session = Depends(deps.get_db)):
    '''
    View all executor shop
    '''
    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_USER_DETAIL_SCOPE)
        executor=crud_user.get_user(db=db,user_id=executor_id)
        if executor is None or executor.role!="executor"   :
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid executor id"
            )
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
    return crud_shop.get_all_shop_of_executor(db=db,executor_id=executor_id)

@router.post("/{executors_id}/add-many-shop")
async def asign_shop_to_executor(executors_id: str,shop_id:List[str],token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    
    try:
        check_sercurity_scopes(token=token,scopes=settings.ADD_EXECUTOR_SHOP_SCOPE)


        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("role")=="manager":
            for id in shop_id:
                if crud_shop.check_shop_manager(db=db,shop_id=id,manager_id=payload.get("id")) is False:
                    raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Shop not belong to your channel"
                )

        executor=crud_user.get_user(db=db,user_id=executors_id)
        if executor is None or executor.role!="executor"   :
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid executor id"
            )

        for id in shop_id:
            if not crud_shop_executor.get_shop_executor(db=db,shop_id=id,executor_id=executors_id) is None:
                raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Executor already exist in shop"
            )
        for id in shop_id:
            crud_shop_executor.create_new_shop_executor(db=db,shop_id=id,executor_id=executors_id)
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
    return {"message":"update success"}

@router.post("/{executors_id}/delete-many-shop")
async def delete_shop_for_executors(executors_id: str,shop_id:List[str],token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    
    try:
        check_sercurity_scopes(token=token,scopes=settings.DELETE_EXECUTOR_SHOP_SCOPE)

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("role")=="manager":
            for id in shop_id:
                if crud_shop.check_shop_manager(db=db,shop_id=id,manager_id=payload.get("id")) is False:
                    raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Shop not belong to your channel"
                )
        executor=crud_user.get_user(db=db,user_id=executors_id)
        if executor is None or executor.role!="executor"   :
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid executor id"
            )

        for id in shop_id:
            if crud_shop_executor.get_shop_executor(db=db,shop_id=id,executor_id=executors_id) is None:
                raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Shop not found"
            )
        for id in shop_id:
            crud_shop_executor.delete_shop_executor(db=db,shop_id=id,executor_id=executors_id)
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
    return {"message":"delete success"}

@router.get("/{executor_id}/all-shop-not-asign", response_model=List[shop_schema.Shop])
def get_all_shops_executor_not_asign(executor_id:str,token:Optional[str] = Header(None), db: Session = Depends(deps.get_db)):
    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_USER_DETAIL_SCOPE)
        executor=crud_user.get_user(db=db,user_id=executor_id)
        if executor is None or executor.role!="executor"   :
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid executor id"
            )
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
    return crud_shop.get_all_not_shop_of_executor(db=db,executor_id=executor_id)

@router.get("/{manager_id}/all-channel", response_model=List[channel_schema.Channel])
def get_all_channel_of_manager(manager_id:str,token:Optional[str] = Header(None), db: Session = Depends(deps.get_db)):
    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_USER_DETAIL_SCOPE)
        executor=crud_user.get_user(db=db,user_id=manager_id)
        if executor is None or executor.role!="manager"   :
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid manager id"
            )
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
    return crud_channel.get_all_channel_of_manager(db=db,manager_id=manager_id)

@router.get("/{manager_id}/all-channel-not-asign", response_model=List[channel_schema.Channel])
def get_all_channel_not_asign_to_manager(manager_id:str,token:Optional[str] = Header(None), db: Session = Depends(deps.get_db)):

    try:
        check_sercurity_scopes(token=token,scopes=settings.VIEW_USER_DETAIL_SCOPE)
        executor=crud_user.get_user(db=db,user_id=manager_id)
        if executor is None or executor.role!="manager":
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid manager id"
            )
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
    return crud_channel.get_all_not_channel_of_manager(db=db,manager_id=manager_id)

@router.post("/{manager_id}/add-channel")
def asign_channel_to_manager(manager_id: str,channel_id:List[str],token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    try:
        check_sercurity_scopes(token=token,scopes=settings.ADD_CHANNEL_MANAGER_SCOPE)
        manager=crud_user.get_user(db=db,user_id=manager_id)
        if manager is None or manager.role!="manager"   :
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid manager id"
            )
        for id in channel_id:
            if crud_channel.get_channel(db=db,channel_id=id) is None:
                raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid channel id"
            )
        for id in channel_id:
            if not crud_channel_manager.get_channel_manager(db=db,channel_id=id,manager_id=manager_id) is None:
                if crud_channel.get_channel(db=db,channel_id=id):
                    raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Channel already asign to manager"
            )
        for id in channel_id:
            crud_channel_manager.create_channel_manager(db=db,manager_id=manager_id,channel_id=id)
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
    return {"message":"update success"}

@router.post("/{manager_id}/delete-channel")
def delete_channel_of_manager(manager_id: str,channel_id:List[str],token:Optional[str] = Header(None),db: Session = Depends(deps.get_db)):
    
    try:
        check_sercurity_scopes(token=token,scopes=settings.DELETE_CHANNEL_MANAGER_SCOPE)


        manager=crud_user.get_user(db=db,user_id=manager_id)
        if manager is None or manager.role!="manager"   :
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid manager id"
            )
        for id in channel_id:
            if crud_channel.get_channel(db=db,channel_id=id) is None:
                raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid channel id"
            )
        for id in channel_id:
            if crud_channel_manager.get_channel_manager(db=db,channel_id=id,manager_id=manager_id) is None:
                if crud_channel.get_channel(db=db,channel_id=id):
                    raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Channel not  asign to manager"
            )
        for id in channel_id:
            crud_channel_manager.delete_channel_manager(db=db,manager_id=manager_id,channel_id=id)
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
    return {"message":"delete success"}