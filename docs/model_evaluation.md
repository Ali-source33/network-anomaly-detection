# Model Değerlendirmesi

**Deneme Yapılan Modeller:**
- Logistic Regression
- Random Forest
- HistGradientBoostingClassifier (Seçilen Final Model)

**Neden HistGradientBoosting?**
En yüksek Recall ve F1 skorunu sağladığı için validation seti üzerinde en iyi aday olarak seçilmiştir.

**Test Sonuçları (Doğrulanmış Gerçek Metrikler):**
- Recall: %99.13
- Precision: %99.57
- F1 Score: %99.35
- Yanlış Pozitif (False Positive): 272
- Yanlış Negatif (False Negative): 554

**Data Leakage (Veri Sızıntısı) Değerlendirmesi:**
Global duplicate temizleme ile birebir kayıt sızıntısı azaltılmıştır.
Preprocessing bileşenleri yalnızca TRAIN üzerinde fit edilmektedir.
Bununla birlikte güvenilir Flow ID ve Timestamp bilgisi bulunmadığından temporal/flow-level leakage tamamen dışlanamaz.

**Veri Bölme (Split) Yöntemi:**
Bu çalışmada veriler **Tabakalı Ardışık Bölme (Stratified Sequential Split)** ile ayrılmıştır. Her saldırı sınıfı kendi mevcut kayıt sırası korunarak Train, Validation ve Test bölümlerine ayrılmıştır. Gerçek Timestamp tabanlı chronological split yapılmamıştır.

**Zero-Day Sınırlaması:**
Bu yaklaşım eğitimde temsil edilmeyen saldırı türlerinin oluşturduğu unseen-attack problemini azaltmayı amaçlamaktadır. Gerçek Zero-Day saldırı tespit performansı bu çalışma kapsamında kanıtlanmamıştır. Model, eğitimde temsil edilen bilinen saldırı türlerini tespit eden supervised saldırı/anomali tespit modelidir.
