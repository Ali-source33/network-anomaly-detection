# Proje Yapısı

- `api/`: FastAPI arka uç sunucusu. `main.py` tahmin endpointlerini barındırır.
- `config/`: Proje sabitlerini (model yolları vb.) barındıran ayarlar.
- `dashboard/`: Streamlit kullanıcı arayüzü.
- `docs/`: Sistem mimarisi ve API detaylarını içeren dökümantasyon klasörü.
- `models/`: Eğitilmiş üretim modeli (`final_model.joblib`).
- `notebooks/`: Veri keşfi ve analiz not defterleri.
- `reports/`: Deneysel süreçleri ve proje çıktılarını belgeleyen markdown raporları.
- `src/`: Veri işleme, eğitim scripti (`train.py`) ve XAI (`xai/explainer.py`) kaynak kodları.
- `tests/`: Sistem ve XAI bütünlük testleri.
