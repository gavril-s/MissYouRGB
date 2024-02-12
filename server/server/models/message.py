from pattern import Pattern
from pydantic import BaseModel


class Message(BaseModel):
    client_id: str
    pattern: Pattern
