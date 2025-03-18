from pydantic import BaseModel


class PredictionIn(BaseModel):
    area: float
    perimeter: float
    major_axis_length: float
    minor_axis_length: float


class PredictionOut(BaseModel):
    class_predicted: list