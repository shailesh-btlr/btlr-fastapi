from typing import List, Optional
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: str
    task_list: str
    business_id: int
    parent_id: Optional[int] = None


class Role(RoleBase):
    id: int


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


RoleList = List[Role]
