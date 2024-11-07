from typing import Optional
from pydantic import BaseModel


class BusinessBase(BaseModel):
    name: str
    prompt: Optional[str] = None


class Business(BusinessBase):
    id: int


class BusinessCreate(BusinessBase):
    pass


class BusinessUpdate(BusinessBase):
    pass
