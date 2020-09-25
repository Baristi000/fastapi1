from typing import List, Optional

from pydantic import BaseModel


class MessageBase(BaseModel):
    id:str
    sim_number:str


class MessageCreate(MessageBase):
    otp: str
    raw_message: str
    time_stamp:str
    shop_id:str

class Message(MessageBase):
    otp: str
    raw_message: str
    time_stamp:str
    shop_id:str

    class Config:
        orm_mode = True