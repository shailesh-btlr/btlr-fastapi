from typing import List
from pydantic import BaseModel
from app.schemas.users import UserBase


class EmployeeBase(BaseModel):
    business_id: int
    user_id: int


class Employee(EmployeeBase):
    id: int
    user: UserBase


class EmployeeCreate(EmployeeBase):
    pass


EmployeeList = List[Employee]
