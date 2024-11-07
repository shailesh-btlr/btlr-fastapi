from pydantic import BaseModel

from app.schemas.auth import Claims


class OpaInput(BaseModel):
    method: str
    path: list[str]
    claims: Claims
