from pydantic import BaseModel


class TouchpointClustereBase(BaseModel):
    name: str


class TouchpointCluster(TouchpointClustereBase):
    id: int


class TouchpointClusterCreate(TouchpointClustereBase):
    pass
