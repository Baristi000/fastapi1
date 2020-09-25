from typing import List, Optional

from pydantic import BaseModel


class Channel_ManagerBase(BaseModel):
    channel_id:str
    manager_id:str


class  Channel_ManagerCreate(Channel_ManagerBase):
    pass

class  Channel_Manager(Channel_ManagerBase):
    pass

    class Config:
        orm_mode = True