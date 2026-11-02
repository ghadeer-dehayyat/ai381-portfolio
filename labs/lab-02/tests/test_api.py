
from fastapi.testclient import TestClient

from src.app.main import app, model

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "model_loaded": True,
    }


def test_model_is_loaded():
    assert model is not None
    assert hasattr(model, "predict_proba")


def test_predict_endpoint():
    customer = {
        "tenure_months": 12,
        "monthly_fee": 70.0,
        "contract": "Month-to-month",
        "internet_service": "Fiber optic",
        "support_calls": 2,
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 200
    assert "churn_probability" in response.json()


def test_invalid_input_is_rejected():
    customer = {
        "tenure_months": -1,
        "monthly_fee": 70.0,
        "contract": "Month-to-month",
        "internet_service": "Fiber optic",
        "support_calls": 2,
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 422


def test_extra_input_is_rejected():
    customer = {
        "tenure_months": 12,
        "monthly_fee": 70.0,
        "contract": "Month-to-month",
        "internet_service": "Fiber optic",
        "support_calls": 2,
        "unknown_field": "unexpected",
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 422
