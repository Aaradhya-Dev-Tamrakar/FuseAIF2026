"""Tests for FastAPI serving endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.serve import app, load_production_model


@pytest.fixture(scope="module", autouse=True)
def setup_model():
    """Load the production model once for all tests."""
    load_production_model()


@pytest.fixture
def client():
    return TestClient(app)


SAMPLE_CUSTOMER = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.35,
    "TotalCharges": 844.2,
}


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_has_model_info(self, client):
        data = client.get("/health").json()
        assert data["status"] == "healthy"
        assert data["model_name"] == "TelcoChurnPredictor"
        assert "model_version" in data


class TestPredictEndpoint:
    def test_predict_returns_200(self, client):
        resp = client.post("/predict", json=SAMPLE_CUSTOMER)
        assert resp.status_code == 200

    def test_predict_has_required_fields(self, client):
        data = client.post("/predict", json=SAMPLE_CUSTOMER).json()
        assert "churn_prediction" in data
        assert "churn_probability" in data
        assert "risk_classification" in data
        assert data["churn_prediction"] in (0, 1)
        assert 0.0 <= data["churn_probability"] <= 1.0
        assert data["risk_classification"] in ("Low", "Medium", "High")

    def test_predict_high_risk_customer(self, client):
        high_risk = SAMPLE_CUSTOMER.copy()
        high_risk["tenure"] = 1
        high_risk["MonthlyCharges"] = 105.0
        high_risk["TotalCharges"] = 105.0
        high_risk["Contract"] = "Month-to-month"
        data = client.post("/predict", json=high_risk).json()
        # High risk profile should have elevated churn probability
        assert data["churn_probability"] > 0.3
