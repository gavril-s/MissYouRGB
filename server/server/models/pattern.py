from pydantic import BaseModel


class RGB(BaseModel):
    red: int
    green: int
    blue: int


class StripState(BaseModel):
    pixels: list[RGB]


class Pattern(BaseModel):
    strip_length: int
    steps: list[StripState]
    step_duration: float
    iterations: int
