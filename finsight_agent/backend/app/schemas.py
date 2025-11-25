from pydantic import BaseModel
from typing import List, Optional
import datetime

class StrategyBase(BaseModel):
    name: str
    description: Optional[str] = None

class StrategyCreate(StrategyBase):
    pass

class Strategy(StrategyBase):
    id: int
    owner_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    strategies: List[Strategy] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class AgentRequest(BaseModel):
    query: str
