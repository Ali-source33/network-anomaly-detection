from fastapi.testclient import TestClient
from api.main import app
import joblib
from config.settings import MODEL_PATH
import json

client = TestClient(app)

def test_xai_endpoint():
    model = joblib.load(MODEL_PATH)
    features = list(model.feature_names_in_)
    valid_payload = {f: 0.0 for f in features}
    valid_payload['Destination Port'] = 80
    valid_payload['Total Fwd Packets'] = 10
    valid_payload['Total Backward Packets'] = 5
    if 'Fwd_Bwd_Ratio' in valid_payload:
        del valid_payload['Fwd_Bwd_Ratio']
        
    res = client.post('/predict', json={'features': valid_payload})
    assert res.status_code == 200
    data = res.json()
    assert "explanation" in data
    assert "top_features" in data["explanation"]
    assert len(data["explanation"]["top_features"]) <= 3
