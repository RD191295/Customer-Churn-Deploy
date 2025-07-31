from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model # type: ignore
import pickle
import os

app = FastAPI()

# Load Model and scaler
MODEL_PATH = os.path.join(os.path.dirname(__file__),"churn_ann.h5")
SCALER_PATH = os.path.join(os.path.dirname(__file__),"scaler.pkl")

model = load_model(MODEL_PATH)
scaler = pickle.load(open(SCALER_PATH,'rb'))


class CustmoerFeatures(BaseModel):
    CreditScore :int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard:int
    IsActiveMember: int
    EstimatedSalary: float

geo_map = {'France': 0 ,  'Spain': 1 ,'Germany': 2}
gender_map = {'male':1 , 'Female':0}

@app.post('/predict')
def predict_churn(features: CustmoerFeatures):
    data = features.model_dump()
    # encode Categorical
    data['Geography'] = geo_map.get(data['Geography'], 0)
    data['Gender'] = gender_map.get(data['Gender'], 0)
    x = pd.DataFrame([data])
    #scale 
    x_scaled = scaler.transform(x)
    pred = model.predict(x_scaled)[0][0]
    return {'churn_probability':float(pred),'churned':int(pred > 0.5)}

