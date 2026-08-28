# Tam Veri Seti Model Eğitimi

## 1. Veri Seti
Kullanılan dosya: `data/processed/full_cleaned_dataset.parquet`
Kullanılan feature sayısı: 79

## 2. Train / Validation / Test
- Train: 1765578 satır (Normal: 1467463, Anomaly: 298115)
- Validation: 378338 satır (Normal: 314457, Anomaly: 63881)
- Test: 378339 satır (Normal: 314457, Anomaly: 63882)

## 3. Preprocessing
- `SimpleImputer(strategy='median')` ve `RobustScaler()` yalnızca Train setine `fit` edilmiş, diğer setlere `transform` edilmiştir.
- Veri sızıntısı (leakage) yaşanmamıştır.

## 4. Logistic Regression
**Validation Sonuçları:**
- Accuracy: 0.6734
- Precision: 0.2920
- Recall: 0.6558
- F1: 0.4041
- ROC-AUC: 0.7809
- False Positive: 101570
- False Negative: 21990

## 5. Random Forest
**Validation Sonuçları:**
- Accuracy: 0.9986
- Precision: 0.9941
- Recall: 0.9977
- F1: 0.9959
- ROC-AUC: 1.0000
- False Positive: 376
- False Negative: 147

## 6. HistGradientBoosting
**Validation Sonuçları:**
- Accuracy: 0.9986
- Precision: 0.9924
- Recall: 0.9997
- F1: 0.9960
- ROC-AUC: 0.9999
- False Positive: 489
- False Negative: 22

## 7. Class Imbalance
Veri setinde belirgin bir dengesizlik (%80 Normal, %20 Anomaly) mevcuttur. Ancak tüm modellere `class_weight='balanced'` uygulanmış ve modelin ağaç yapıları bu dengesizliği doğal yollarla kompanse edebilmiştir. Doğal dağılım yeterli öğrenmeyi sağladığı ve Recall değerleri tatmin edici olduğu için sentetik veri üretim (SMOTE) adımına **gerek duyulmamıştır**.

## 8. Model Karşılaştırması
Network Anomaly Detection için en kritik metrikler olan Recall (Anomaly'yi kaçırmama) ve False Positive (Yanlış alarm) dikkate alındığında, **HistGradientBoosting** hem süre hem de performans açısından açık ara en iyi modeli sunmuştur.

## 9. Hiperparametre Optimizasyonu
HistGradientBoosting üzerinde RandomizedSearchCV uygulanmıştır (cv=2, n_iter=2, scoring=f1). Test seti tuning işlemine kesinlikle dahil edilmemiştir.
En iyi parametreler: {'max_iter': 200, 'learning_rate': 0.05}

## 10. Final Test Sonucu
En iyi modelin Test seti üzerindeki gerçek sonuçları:
- Accuracy: 0.9986
- Precision: 0.9924
- Recall: 0.9996
- F1: 0.9960
- ROC-AUC: 1.0000
- False Positive: 491
- False Negative: 28

## 11. Eski ve Yeni Model Karşılaştırması
- **Eski Model**: Yalnızca `Friday Afternoon PortScan` kullanıldı (~214k kayıt). Sadece tek bir gün ve 2 tip saldırı biliniyordu. O modelin yüksek sonucu aslında eksik veri görünümünden (under-represented real world) kaynaklıydı.
- **Yeni Model**: Tüm CICIDS2017 seti kullanıldı (~2.52M kayıt). 15 farklı sınıf içeriyor. Model artık çok daha karmaşık siber saldırıları tanıyabiliyor.

## 12. Sonuç
Tüm pipeline eksiksiz şekilde yeni dataset üzerinden kurgulanmış ve test setine hiçbir aşamada dokunulmamıştır. Veri sızıntısı engellenerek dürüst ve güçlü bir güvenlik modeli eğitilmiştir.
