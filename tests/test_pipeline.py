import pytest
from fastapi.testclient import TestClient
import pandas as pd
import joblib
import os
import sys

# API import için path ayarı
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_model_exists():
    model_path = os.path.join("models", "final_model.joblib")
    assert os.path.exists(model_path), "Final model file does not exist."
    model = joblib.load(model_path)
    assert model is not None, "Failed to load the model."

def test_predict_endpoint_missing_input():
    # Hatalı İstek Testi
    response = client.post("/predict", json={})
    assert response.status_code == 422 # Unprocessable Entity
