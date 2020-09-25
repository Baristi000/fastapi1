from typing import List, Optional

from pydantic import BaseModel


class CountryBase(BaseModel):
    name:str


class CountryCreate(CountryBase):
    postl_code:str

class Country(CountryBase):
    postl_code:str

    class Config:
        orm_mode = True