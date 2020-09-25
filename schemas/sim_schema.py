from typing import List, Optional

from pydantic import BaseModel


class SimBase(BaseModel):
    sim_number:str


class SimCreate(SimBase):
    tty_gateway: str
    status:str

class Sim(SimBase):
    tty_gateway: str
    status:str

    class Config:
        orm_mode = True