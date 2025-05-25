from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime


class CombinationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    items: List[Dict[str, Any]] = Field(..., min_items=1)
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class CombinationCreate(CombinationBase):
    pass


class CombinationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    items: Optional[List[Dict[str, Any]]] = Field(None, min_items=1)
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class CombinationInDB(CombinationBase):
    id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class CombinationResponse(CombinationInDB):
    owner: Optional[Dict[str, Any]] = None
