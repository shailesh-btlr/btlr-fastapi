from typing import List, Optional
from pydantic import BaseModel


class DepartmentBase(BaseModel):
    name: str
    business_id: int
    parent_id: Optional[int] = None


class Department(DepartmentBase):
    id: int


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdateBase(BaseModel):
    name: str


class DepartmentUpdate(DepartmentUpdateBase):
    pass


DepartmentList = List[Department]
