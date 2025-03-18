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
    data = pd.DataFrame([[payload.Area, payload.Perimeter, payload.MajorAxisLength, payload.MinorAxisLength]], 
                    columns=['Area', 'Perimeter', 'MajorAxisLength', 'MinorAxisLength'])
    prediction = model.predict(data)
    logger.info(f"Prediction: {prediction}")
    return {"class_predicted": prediction.tolist()}