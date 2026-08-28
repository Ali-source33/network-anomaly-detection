# Final Model Eğitimi
## 1. Veri Seti
Kullanılan feature sayısı: 79. Orijinal veri setinden 8 dosya kullanılmıştır.

## 2. Day-Based Split
- **Train:** Pazartesi, Salı, Çarşamba
- **Validation:** Perşembe
- **Test:** Cuma

## 3. Train Verisi
- Toplam Satır: 1503571
- Normal: 1300759, Anomaly: 202812

## 4. Validation Verisi
- Toplam Satır: 402139
- Normal: 399960, Anomaly: 2179

## 5. Test Verisi
- Toplam Satır: 615847
- Normal: 395059, Anomaly: 220788

## 6. Preprocessing
- Yalnızca TRAIN verisinde fit işlemi yapılmış, Val ve Test setlerinde sadece transform uygulanmıştır.
- Target ve Original_Label eğitimde feature olarak kullanılmamıştır.

## 7. Model Karşılaştırması
Validation Seti Sonuçları:
- **Logistic Regression**: F1: 0.0624, Recall: 0.8421, FP: 54805, FN: 344
- **Random Forest**: F1: 0.0308, Recall: 0.0188, FP: 444, FN: 2138
- **HistGradientBoosting**: F1: 0.8865, Recall: 0.8692, FP: 200, FN: 285

## 8. Class Imbalance
- Train setindeki dengesizliğe karşı Scikit-Learn 1.3+ ile desteklenen `class_weight='balanced'` parametresi HGB dahil tüm modellerde kullanılmış, SMOTE'a ihtiyaç duyulmamıştır.

## 9. Hyperparameter Tuning
- HGB için en uygun konfigürasyon (`learning_rate=0.05`, `max_iter=200`, `class_weight='balanced'`) üzerinden ilerlenmiştir.

## 10. Final Test Sonuçları
Tamamen yalıtılmış Cuma test seti (Sıfırıncı gün saldırıları) üzerindeki sonuçlar:
- **Accuracy**: 0.7703
- **Precision**: 0.9980
- **Recall**: 0.3600
- **F1**: 0.5291
- **ROC-AUC**: 0.7787

## 11. Confusion Matrix
Test seti CM:
```
TP (Doğru Saldırı Tespiti): 79475
TN (Doğru Normal Tespiti): 394896
FP (Yanlış Alarm): 163
FN (Kaçırılan Saldırı): 141313
```

## 12. False Positive / False Negative
- FP: 163
- FN: 141313

## 13. Random Split ile Karşılaştırma
- Eski Random split yöntemindeki %99.86 Accuracy, test setinde aynı saldırının parçacıkları olduğu için son derece iyimser (optimistic) bir tabloydu.
- Day-based test sonuçları ise modelin yepyeni saldırı (Cuma günü DDoS ve PortScan) imzasını yakalama kabiliyetini dürüstçe ölçen final performansıdır.

## 14. Leakage Değerlendirmesi
- Preprocessing/statistical leakage: YOK (Sadece Train fit edildi)
- Train/Test index overlap: YOK (Günlere göre fiziksel ayırma yapıldı)
- Identical row overlap: YOK (Split öncesinde global deduplication yapıldı)
- Flow/domain-level leakage: Flow ID, Source IP ve Timestamp mevcut olmadığı için %100 leakage-free garantisi tam ölçülemiyor olsa da, Day-based split ile bu risk rastgele bölmeye kıyasla çok ciddi oranda azaltılmış ve sıfıra yaklaştırılmıştır.

## 15. Sonuç
- Model gerçek hayat (Zero-Day) senaryosuna en yakın şekilde eğitilmiş ve Production adayı olarak seçilmiştir.
