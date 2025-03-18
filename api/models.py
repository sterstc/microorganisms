from pydantic import BaseModel


class PredictionIn(BaseModel):
    Area: float
    Perimeter: float
    MajorAxisLength: float
    MinorAxisLength: float

class PredictionOut(BaseModel):
    class_predicted: list