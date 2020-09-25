from typing import List, Optional

from pydantic import BaseModel


class ChannelBase(BaseModel):
    name:str


class ChannelCreate(ChannelBase):
    id:str

class Channel(ChannelBase):
    id:str

    class Config:
        orm_mode = True