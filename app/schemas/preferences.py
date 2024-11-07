from typing import List

from pydantic import BaseModel


class Preference(BaseModel):
    name: str


class PreferenceAdd(Preference):
    parent_id: str
    user_id: str


class PreferenceTree(Preference):
    children: List["PreferenceTree"]


class PreferenceTreeAdd(BaseModel):
    tree: PreferenceTree
    user_id: str
