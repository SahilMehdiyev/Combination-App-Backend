from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    acces_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str
