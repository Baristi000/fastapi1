from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str


class UserCreate(UserBase):
    id: str
    role: str
    activate:str

class User(UserBase):
    id: str
    role: str
    activate:str
    hashed_password:Optional[str] = None
    first_name:Optional[str] = None
    last_name:Optional[str] = None
    last_login:Optional[str] = None

    class Config:
        orm_mode = True