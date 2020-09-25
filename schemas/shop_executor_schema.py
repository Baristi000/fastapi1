from typing import List, Optional

from pydantic import BaseModel


class Shop_ExecutorBase(BaseModel):
    shop_id:str
    executor_id:str


class  Shop_ExecutorCreate(Shop_ExecutorBase):
    def __init__(self, shop_id, executor_id):
        self.shop_id = shop_id
        self.executor_id = executor_id

    pass

class  Shop_Executor(Shop_ExecutorBase):
    pass

    class Config:
        orm_mode = True