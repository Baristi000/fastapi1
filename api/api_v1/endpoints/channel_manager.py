from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

import crud, models, schemas
from crud import crud_channel_manager,crud_user,crud_channel
from schemas import channel_manager_schema
from api import deps
router = APIRouter()


@router.post("/")
def add(channel_id:str,manager_id:str,db:Session = Depends(deps.get_db)):
    crud_channel_manager.create_channel_manager(db=db,manager_id=manager_id,channel_id=channel_id)