from pydantic import BaseModel
from app.schemas.roles import Role


class TouchpointRoleBase(BaseModel):
    prompt: str
    role_id: int


class TouchpointRole(TouchpointRoleBase):
    id: int
    role: Role


class TouchpointRoleCreate(TouchpointRoleBase):
    pass


class TouchpointRoleUpdate(TouchpointRoleBase):
    pass
