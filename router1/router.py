from fastapi import APIRouter, FastAPI
import random

router = APIRouter();

@router.get("/get-in/{username}")
def get_in():
    return {"username":username,
            "pass_generator": random.randint(1, 100000)}