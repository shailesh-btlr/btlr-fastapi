from pydantic import BaseModel


class Image(BaseModel):
    name: str
    format: str
