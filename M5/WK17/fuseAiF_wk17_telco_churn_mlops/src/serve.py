"""FastAPI model serving endpoint for the Telco Customer Churn production model.

Loads the MLflow-registered 'TelcoChurnPredictor' model and exposes:
  - GET  /health   : Service health, model version, loaded stage
  - POST /predict  : Accept customer profile, return churn prediction + probability + risk tier
"""

from __future__ import annotations

import os
import time

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"

MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
REGISTERED_MODEL_NAME = "TelcoChurnPredictor"

# ---------- Pydantic schemas ----------


class CustomerProfile(BaseModel):
    """Input schema for a single customer churn prediction request."""

    gender: str = Field(examples=["Female"])
    SeniorCitizen: int = Field(ge=0, le=1, examples=[0])
    Partner: str = Field(examples=["Yes"])
    Dependents: str = Field(examples=["No"])
    tenure: int = Field(ge=0, examples=[12])
    PhoneService: str = Field(examples=["Yes"])
    MultipleLines: str = Field(examples=["No"])
    InternetService: str = Field(examples=["Fiber optic"])
    OnlineSecurity: str = Field(examples=["No"])
    OnlineBackup: str = Field(examples=["Yes"])
    DeviceProtection: str = Field(examples=["No"])
    TechSupport: str = Field(examples=["No"])
    StreamingTV: str = Field(examples=["No"])
    StreamingMovies: str = Field(examples=["No"])
    Contract: str = Field(examples=["Month-to-month"])
    PaperlessBilling: str = Field(examples=["Yes"])
    PaymentMethod: str = Field(examples=["Electronic check"])
    MonthlyCharges: float = Field(ge=0, examples=[70.35])
    TotalCharges: float = Field(ge=0, examples=[844.2])


class PredictionResponse(BaseModel):
    """Output schema for churn prediction."""

    churn_prediction: int = Field(description="Binary prediction: 1=Churn, 0=Retained")
    churn_probability: float = Field(description="Probability of churn (0.0 to 1.0)")
    risk_classification: str = Field(description="Risk tier: Low, Medium, or High")
    model_name: str
    model_version: str


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str
    model_name: str
    model_version: str
    model_stage: str
    uptime_seconds: float


# ---------- Application ----------

app = FastAPI(
    title="Telco Customer Churn Prediction API",
    description="Production-grade FastAPI serving endpoint for the MLflow-registered TelcoChurnPredictor model.",
    version="1.0.0",
)

# Global state loaded at startup
_model = None
_model_version = "unknown"
_model_stage = "unknown"
_start_time = time.time()


def load_production_model():
    """Load the production model from MLflow Model Registry."""
    global _model, _model_version, _model_stage  # noqa: PLW0603

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    # Try alias-based loading first (MLflow 2.x+), fall back to stage-based
    try:
        model_uri = f"models:/{REGISTERED_MODEL_NAME}@production"
        _model = mlflow.sklearn.load_model(model_uri)
        _model_stage = "production (alias)"
    except Exception:
        try:
            model_uri = f"models:/{REGISTERED_MODEL_NAME}/Production"
            _model = mlflow.sklearn.load_model(model_uri)
            _model_stage = "Production (stage)"
        except Exception:
            # Fallback: load latest version
            from mlflow.tracking import MlflowClient

            client = MlflowClient(MLFLOW_TRACKING_URI)
            versions = client.search_model_versions(f"name='{REGISTERED_MODEL_NAME}'")
            if not versions:
                raise RuntimeError(
                    f"No model versions found for '{REGISTERED_MODEL_NAME}'. Run src/train.py first."
                )
            latest = max(versions, key=lambda v: int(v.version))
            model_uri = f"models:/{REGISTERED_MODEL_NAME}/{latest.version}"
            _model = mlflow.sklearn.load_model(model_uri)
            _model_stage = f"v{latest.version} (fallback)"

    # Extract version number
    from mlflow.tracking import MlflowClient

    client = MlflowClient(MLFLOW_TRACKING_URI)
    versions = client.search_model_versions(f"name='{REGISTERED_MODEL_NAME}'")
    if versions:
        prod_versions = [v for v in versions if v.current_stage == "Production"]
        if prod_versions:
            _model_version = str(prod_versions[0].version)
        else:
            _model_version = str(max(versions, key=lambda v: int(v.version)).version)

    print(f"[serve.py] Loaded model '{REGISTERED_MODEL_NAME}' v{_model_version} ({_model_stage})")


def classify_risk(probability: float) -> str:
    """Map churn probability to human-readable risk classification."""
    if probability >= 0.7:
        return "High"
    elif probability >= 0.4:
        return "Medium"
    else:
        return "Low"


@app.on_event("startup")
async def startup_event():
    """Load model from MLflow registry on server startup."""
    load_production_model()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Service health check with model version and uptime."""
    if _model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return HealthResponse(
        status="healthy",
        model_name=REGISTERED_MODEL_NAME,
        model_version=_model_version,
        model_stage=_model_stage,
        uptime_seconds=round(time.time() - _start_time, 2),
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict_churn(profile: CustomerProfile):
    """Predict customer churn from a single customer profile."""
    if _model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    input_df = pd.DataFrame([profile.model_dump()])

    try:
        prediction = int(_model.predict(input_df)[0])
        probabilities = _model.predict_proba(input_df)[0]
        churn_prob = float(probabilities[1])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    return PredictionResponse(
        churn_prediction=prediction,
        churn_probability=round(churn_prob, 4),
        risk_classification=classify_risk(churn_prob),
        model_name=REGISTERED_MODEL_NAME,
        model_version=_model_version,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.serve:app", host="0.0.0.0", port=8000, reload=False)
