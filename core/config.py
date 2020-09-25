import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator
from urllib.parse import quote_plus

class Settings(BaseSettings):
    MYSQL_SERVER :str ="127.0.0.1"
    MYSQL_PORT :int =3306
    MYSQL_PASSWORD :str ="T123"
    MYSQL_USER:str ="trieu"
    MYSQL_DB:str ="sim_card_management"
    SQLACHEMY_CONNECTION_STRING = 'mysql+pymysql://{}:{}@{}/{}'.format(MYSQL_USER,quote_plus(MYSQL_PASSWORD), MYSQL_SERVER, MYSQL_DB)
    
    REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    SECRET_KEY:str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1000
    ADD_NEW_USER="Add new user"
    VIEW_ALL_USER_SCOPE="View all user"
    VIEW_ALL_SHOP_SCOPE="View all shop"
    VIEW_ALL_SIM_SCOPE="View all sim"
    VIEW_ALL_CHANNEL_SCOPE="View all channel"
    VIEW_USER_DETAIL_SCOPE="View user details"
    VIEW_SHOP_DETAIL_SCOPE="view shop details"
    VIEW_CHANNEL_DETAIL_SCOPE="View Channel details"
    VIEW_SIM_DETAIL_SCOPE="View sim details"
    ADD_EXECUTOR_SHOP_SCOPE="Add shop executor"
    DELETE_EXECUTOR_SHOP_SCOPE="Delete shop executor"
    UPDATE_SHOP_SIM_SCOPE="Update shop sim number"
    ADD_CHANNEL_MANAGER_SCOPE="Add channel manager"
    DELETE_CHANNEL_MANAGER_SCOPE="Delete channel manager"
    INACTIVATE_USER_SCOPE="Inactivate user"
    UPDATE_USER_ROLE_SCOPE="Update user role"
    ADMIN_SCOPE="All"

    NEWUSER_SCOPES=[
        VIEW_ALL_USER_SCOPE,
        VIEW_ALL_SHOP_SCOPE,
        VIEW_ALL_SIM_SCOPE,
        VIEW_ALL_CHANNEL_SCOPE,
        VIEW_USER_DETAIL_SCOPE,
        VIEW_SHOP_DETAIL_SCOPE,
        VIEW_CHANNEL_DETAIL_SCOPE,
        VIEW_SIM_DETAIL_SCOPE,
        ]
    EXECUTOR_SCOPES=[
        UPDATE_SHOP_SIM_SCOPE,
        VIEW_ALL_USER_SCOPE,
        VIEW_ALL_SHOP_SCOPE,
        VIEW_ALL_SIM_SCOPE,
        VIEW_ALL_CHANNEL_SCOPE,
        VIEW_USER_DETAIL_SCOPE,
        VIEW_SHOP_DETAIL_SCOPE,
        VIEW_CHANNEL_DETAIL_SCOPE,
        VIEW_SIM_DETAIL_SCOPE,
        ]
    MANAGER_SCOPES=[
        UPDATE_SHOP_SIM_SCOPE,
        ADD_EXECUTOR_SHOP_SCOPE,
        DELETE_EXECUTOR_SHOP_SCOPE,
        VIEW_ALL_USER_SCOPE,
        VIEW_ALL_SHOP_SCOPE,
        VIEW_ALL_SIM_SCOPE,
        VIEW_ALL_CHANNEL_SCOPE,
        VIEW_USER_DETAIL_SCOPE,
        VIEW_SHOP_DETAIL_SCOPE,
        VIEW_CHANNEL_DETAIL_SCOPE,
        VIEW_SIM_DETAIL_SCOPE,
        ]
    ADMIN_SCOPES=[
        ADMIN_SCOPE
    ]
    
    class Config:
        case_sensitive = True
settings = Settings()