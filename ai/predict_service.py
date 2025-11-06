# ai/predict_service.py

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="Binance AI Prediction Service", version="1.0")

# ✅ Fix model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")
MODEL_PATH = os.path.abspath(MODEL_PATH)

print("🔍 Loading model from:", MODEL_PATH)
model = joblib.load(MODEL_PATH)
print("✅ Model loaded successfully")

# Define input schema
class CandleInput(BaseModel):
    close: float
    ma3: float
    ma8: float
    rsi: float
    ema_fast: float
    ema_slow: float
    macd: float
    stoch_k: float
    stoch_d: float

@app.post("/predict")
def predict(data: CandleInput):
    try:
        features = np.array([
            [
                data.close,
                data.ma3,
                data.ma8,
                data.rsi,
                data.ema_fast,
                data.ema_slow,
                data.macd,
                data.stoch_k,
                data.stoch_d,
            ]
        ])
        prediction = model.predict(features)[0]
        proba = model.predict_proba(features)[0].max()

        return {
            "prediction": "BUY" if prediction == 1 else "SELL",
            "confidence": round(float(proba), 3),
        }
    except Exception as e:
        return {"error": str(e)}
