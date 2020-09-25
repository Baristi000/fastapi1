from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

import crud, models, schemas
from crud import crud_shop_executor,crud_shop,crud_user
from schemas import shop_executor_schema
from api import deps
router = APIRouter()


