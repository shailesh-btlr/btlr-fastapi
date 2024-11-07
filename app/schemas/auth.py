from typing import Union
from pydantic import BaseModel


class Claims(BaseModel):
    sub: str
    exp: Union[int, None]
    email: Union[str, None]
    scopes: list[str]


class Refresh(BaseModel):
    sub: str
    exp: Union[int, None]
    scopes: list[str]
    uuid: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str
    access_type: str = "bearer"
