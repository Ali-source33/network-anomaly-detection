# API Dokümantasyonu

**Görevi:** Eğitilmiş modeli kullanarak dış dünyadan gelen isteklere tahmin ve açıklanabilirlik (XAI) dönmek.

**Endpoint:** `POST /predict`
**Beklenen Input (JSON):**
```json
{
    "features": {
        "Flow Duration": 1234,
        ... (toplam 78/79 feature)
    }
}
```
**Response Formatı:**
```json
{
    "prediction": 0,
    "probability": 0.0012,
    "class": "Normal",
    "explanation": {
        "top_features": [...]
    }
}
```
**Hata Durumları:** Eksik feature gönderilmesi halinde `422 Unprocessable Entity` döner. Model yüklenemezse `503 Service Unavailable`.
