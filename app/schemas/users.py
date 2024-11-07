from pydantic import BaseModel
from typing import List


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int


UserList = List[User]
