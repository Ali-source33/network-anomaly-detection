from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from src.xai.explainer import PerturbationExplainer
import pandas as pd
import os
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Network Anomaly Detection API", version="1.0.0")

from config.settings import MODEL_PATH
model_path = MODEL_PATH
if os.path.exists(model_path):
    model = joblib.load(model_path)
    explainer = PerturbationExplainer(model)
else:
    model = None
    explainer = None

class PredictRequest(BaseModel):
    features: Dict[str, Any]

@app.get("/")
def read_root():
    logger.info("Health check endpoint called.")
    return {"message": "Network Anomaly Detection API is running. Send POST requests to /predict"}

@app.post("/predict")
def predict(request: PredictRequest):
    if model is None:
        logger.error("Predict endpoint called but model is not loaded.")
        raise HTTPException(status_code=503, detail="Model is not loaded.")
    
    try:
        # Veri Dönüştürme
        df = pd.DataFrame([request.features])
        
        # Feature Doğrulama ve Tamamlama
        if hasattr(model, "feature_names_in_"):
            expected_features = list(model.feature_names_in_)
            
            # Fwd_Bwd_Ratio kontrolü
            if "Fwd_Bwd_Ratio" not in df.columns:
                if "Total Fwd Packets" in df.columns and "Total Backward Packets" in df.columns:
                    df["Fwd_Bwd_Ratio"] = df["Total Fwd Packets"] / (df["Total Backward Packets"] + 1e-5)
            
            missing_features = [f for f in expected_features if f not in df.columns]
            if missing_features:
                raise HTTPException(status_code=422, detail=f"Missing features ({len(missing_features)}): {missing_features[:5]}...")
            
            # Sıralamayı garantiye al
            df = df[expected_features]
        
        # Tahmin
        prediction = model.predict(df)[0]
        
        # Olasılık Hesaplama
        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(df)[0][1])
        else:
            probability = 1.0 if prediction == 1 else 0.0
            
        class_name = "Anomaly" if prediction == 1 else "Normal"
        
        # XAI
        explanation = explainer.explain(df, top_k=3) if explainer else []
        
        return {
            "prediction": int(prediction),
            "probability": probability,
            "class": class_name,
            "explanation": {"top_features": explanation}
        }
    except HTTPException as e:
        logger.warning(f"Validation/HTTP Error: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
