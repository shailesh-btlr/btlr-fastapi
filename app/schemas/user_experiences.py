import datetime
from typing import Optional
from pydantic import BaseModel


class CheckIn(BaseModel):
    user_id: int
    business_id: int


class UserExperience(CheckIn):
    id: int
    state: str
    assigned_department_id: Optional[int]
    assigned_role_id: Optional[int]
    assigned_user_id: Optional[int]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ExperienceAssignment(BaseModel):
    department_id: int
    role_id: Optional[int]
    user_id: Optional[int]


class AssignmentAcceptance(BaseModel):
    department_id: int
    role_id: int
    user_id: int
