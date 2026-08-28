# Sistem Mimarisi

Bu belge Network Anomaly Detection projesinin üretim (production) mimarisini açıklamaktadır.

## Genel Sistem Mimarisi
Proje, veri alımından son kullanıcı gösterimine kadar modüler bir yapıya sahiptir.

**Veri Akışı:**
Data (Raw) → Preprocessing (Train/Test Split) → Model Eğitimi (HGB) → Model Kaydı (.joblib) → FastAPI (Inference) → Streamlit Dashboard (UI)

## Production Bileşenleri
1. **Model:** `models/final_model.joblib` (HistGradientBoostingClassifier, 79 feature)
2. **API:** `api/main.py` (FastAPI)
3. **UI:** `dashboard/app.py` (Streamlit)
