from pydantic import BaseModel, ValidationError
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class Token_body(BaseModel):
    access_token: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []