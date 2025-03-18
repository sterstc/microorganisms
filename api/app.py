from .app_config import PATH_TO_MODEL
from .utils import load_model
from .models import PredictionIn, PredictionOut
from fastapi import FastAPI
import pandas as pd
from loguru import logger
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/predict', response_model=PredictionOut, status_code=200)
def predict(payload: PredictionIn):
    model = load_model(PATH_TO_MODEL)
    logger.info(f"Model loaded from {PATH_TO_MODEL}")
    area = payload.area
    perimeter = payload.perimeter
    major_axis_length = payload.major_axis_length
    minor_axis_length = payload.minor_axis_length
    data = pd.DataFrame([[area, perimeter, major_axis_length, minor_axis_length]], columns=['Area', 'Perimeter', 'MajorAxisLength', 'MinorAxisLength'])
    prediction = model.predict(data)
    logger.info(f"Prediction: {prediction}")
    return {"class_predicted": prediction.tolist()}