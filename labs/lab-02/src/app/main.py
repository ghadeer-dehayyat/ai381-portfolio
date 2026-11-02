
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

# Project root: AI381-Lab2/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "model.joblib"

FEATURES = [
    "tenure_months",
    "monthly_fee",
    "contract",
    "internet_service",
    "support_calls",
]


class CustomerInput(BaseModel):
    """Validate the customer data sent to the prediction API."""

    model_config = ConfigDict(extra="forbid")

    tenure_months: int = Field(ge=0)
    monthly_fee: float = Field(ge=0)
    contract: str = Field(min_length=1)
    internet_service: str = Field(min_length=1)
    support_calls: int = Field(ge=0)


app = FastAPI(
    title="AI381 Lab 2 Churn Prediction API",
    version="1.0.0",
)

# Load the trained model from the project root.
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    """Report service health if the application has started."""
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
def predict(customer: CustomerInput):
    """Predict the probability that a customer will churn."""
    customer_data = customer.model_dump()

    X = pd.DataFrame([customer_data], columns=FEATURES)
    probability = float(model.predict_proba(X)[0, 1])

    return {"churn_probability": round(probability, 3)}
