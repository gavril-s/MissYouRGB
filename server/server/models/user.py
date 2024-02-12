from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    strip_length: int
