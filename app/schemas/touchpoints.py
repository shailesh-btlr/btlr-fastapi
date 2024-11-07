from pydantic import BaseModel
from typing import List
from app.schemas.departments import Department
from app.schemas.businesses import Business
from app.schemas.touchpoint_clusters import TouchpointCluster
from app.schemas.touchpoint_roles import TouchpointRole


class TouchpointBase(BaseModel):
    name: str
    description: str
    business_id: int
    department_id: int


class Touchpoint(TouchpointBase):
    id: int
    department: Department
    business: Business
    touchpoint_clusters: List[TouchpointCluster]
    touchpoint_roles: List[TouchpointRole]


class TouchpointCreate(TouchpointBase):
    pass


class TouchpointUpdate(TouchpointBase):
    pass


TouchpointList = List[Touchpoint]
