# Model Envanteri ve Production Mimarisi

Mevcut `models/` dizininde yapılan inceleme sonucunda aşağıdaki model dosyaları tespit edilmiştir. Projedeki karmaşayı önlemek adına hangi dosyaların ne amaçla üretildiği ve hangilerinin güvenle silinebileceği raporlanmıştır.

## 1. Model Envanteri Tablosu

| Dosya | Model | Eğitim Verisi | Kullanıldığı Yer | Production? | Durum |
|------|------|---------------|------------------|-------------|-------|
| `final_model.joblib` | HistGradientBoosting | Tek CSV (Friday PortScan) / Random Split | `api/main.py` (API) ve `dashboard/app.py` (API üzerinden) | Evet (Şu anki) | Aktif olarak API tarafından kullanılıyor. İlerleyen aşamada Day-Based model ile değiştirilecek. |
| `final_model_backup.joblib` | HistGradientBoosting | Tek CSV (Friday PortScan) / Random Split | Hiçbir yer | Hayır | Orijinal `final_model.joblib` yedeği. **Güvenle silinebilir.** |
| `full_dataset_model.joblib` | HistGradientBoosting | 8 CSV (Tam Set) / Random Split | Deneysel analiz scriptleri | Hayır | Leakage barındıran (%99.9 Accuracy) deneysel model. **Güvenle silinebilir.** |
| `final_model_new.joblib` | HistGradientBoosting | 8 CSV (Tam Set) / Day-Based Split | Hata analizi raporları (`error_analysis.py` vb.) | Hayır (Henüz) | Day-Based pipeline ile üretilen, gerçek dünya testlerinden (Cuma %36 Recall) geçmiş yeni aday model. İlerleyen aşamada `final_model.joblib`'in yerini alacaktır. |

## 2. API ve Dashboard'un Kullandığı Model

Yapılan kod incelemesinde:
- **`api/main.py`**: Doğrudan `models/final_model.joblib` dosyasını `joblib.load()` ile belleğe alıp `/predict` endpoint'i üzerinden tahmin sunmaktadır.
- **`dashboard/app.py`**: Model dosyasını doğrudan yüklemez; tahmin almak için FastAPI'nin (`api/main.py`) çalıştırdığı `http://127.0.0.1:8000/predict` adresine HTTP POST isteği atar. Dolayısıyla Dashboard da dolaylı olarak API'nin yüklediği `models/final_model.joblib` modelini kullanmaktadır.

## 3. Hedeflenen Production Mimarisi

Uygulamanın çalışması için birden fazla modele ihtiyaç yoktur. Mevcut karmaşayı gidermek adına **TEK MODEL** yaklaşımı benimsenmelidir.

**TEK MODEL:** `models/final_model.joblib`

**Akış:**
- **API** → Yalnızca `models/final_model.joblib` dosyasını okur.
- **Dashboard** → API'ye bağlanır.

## 4. Sonuç ve Silinebilir Dosyalar

Şu anda API ve Dashboard sadece `final_model.joblib` dosyasına bağlıdır. Bu nedenle:
- `final_model_backup.joblib`
- `full_dataset_model.joblib`
- `final_model_new.joblib` (İçeriği `final_model.joblib`'e aktarıldıktan sonra)

dosyaları production tarafında gereksizdir. Bir sonraki onaylı aşamada, yeni Day-Based model `final_model.joblib` adıyla kaydedilerek diğer tüm gereksiz `.joblib` dosyaları temizlenecektir.
