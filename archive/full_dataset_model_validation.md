# Tam Veri Seti Model Doğrulama ve Analiz Raporu

Kullanıcının talebi üzerine `reports/full_dataset_model_training.md` sonuçları, kullanılan pipeline mantığı ve `full_dataset_model.joblib` modeli teknik düzeyde incelenmiş ve doğrulanmıştır.

## Analiz Edilen Noktalar

### 1. HistGradientBoosting Hangi Preprocessing Adımlarıyla Eğitildi?
Model tam olarak şu Pipeline ile eğitildi:
`Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', RobustScaler())])`
Bu işlemler yalnızca sayısal olan 79 özelliğe uygulandı. Ardından `HistGradientBoostingClassifier(class_weight='balanced', learning_rate=0.05, max_iter=200)` çalıştırıldı. 

### 2. Test Seti Preprocessing Sırasında Fit Edildi Mi?
**Hayır.** Pipeline mantığı gereği (`pipeline.fit(X_train, y_train)`), `imputer` ve `scaler` nesneleri sadece `X_train` üzerinde `fit` edilmiş, Test ve Validation setlerine sadece `transform` uygulanmıştır.

### 3. Validation veya Test Verisinin Bir İstatistiği Train'e Sızdı Mı?
**Hayır.** Veri seti indeks bazlı olarak `scratch/prepare_split.py` içerisinde önceden 3'e (`split_indices.npz`) bölünmüş ve script sadece `train_idx` ile Preprocessing işlemlerini öğrenmiştir. İstatistiksel bir sızıntı yoktur.

### 4. Target veya Original_Label Modele Girdi Mi?
**Hayır.** Veri seti toplam 81 kolondan oluşmaktadır. `X = df.drop(columns=['Target', 'Original_Label'])` adımıyla bu iki kolon silinmiş, modele tam olarak 79 feature girmiştir.

### 5. Duplicate Temizliği Ne Zaman Yapıldı?
Duplicate temizliği **split (bölme) öncesinde**, tüm raw veriler tek DataFrame'de birleştirildikten sonra `scratch/prepare_data.py` içerisinde yapılmıştır. Birebir kopyalar temizlendikten sonra Train/Val/Test ayrımı yapılmıştır.

### 6. Train ve Test Arasında Birebir Aynı Satır Var Mı?
**İndeks bazında hayır.** `train_idx` ve `test_idx` kümelerinin kesişimi `0`'dır. 
Ancak, özellik (feature) vektörü olarak birebir aynı olmasına rağmen **farklı etiketlere (Label)** sahip 23.333 satır tespit edilmiştir (Label Noise). 

### 7. Random Stratified Split ve "Benzer Network Flow" Dağılma Riski
**EVET, ÇOK YÜKSEK RİSK.** CICIDS2017 veri seti "Flow" (Ağ Akışı) bazlıdır. Bir siber saldırı veya normal bağlantı süreci (flow), saniyeler içinde birden fazla paket ve benzer flow-interval satırları üretebilir. Random Stratified Split uygulandığı için, aynı IP/Port ikilisinden gelen (aynı saldırı akışına ait) paketlerin bir kısmı Train setine, çok benzer olan bir kısmı ise Test setine rastgele dağılmıştır. Bu durum **Data Leakage (Flow-Level / Time-Series Leakage)** yaratır.

### 8. ROC-AUC = 1.0000 Neden Bu Kadar Yüksek?
Kusursuz veya 1.0'a çok yakın ROC-AUC skoru **Flow-Level Leakage** (Ağ Akışı Sızıntısı) kaynaklıdır. Test setindeki "görülmemiş" saldırılar aslında Train setinde görülen saldırıların milisaniyeler sonraki kopyalarına çok benzediği için model genel bir siber güvenlik kuralları dizisi öğrenmek yerine, **veriyi ezberlemiş (Overfitting/Memorization)** durumdadır. Test setinin bağımsızlığı zedelenmiştir.

### 9. False Positive = 491 ve False Negative = 28 Değerleri Doğru Mu?
**Doğrudur.** Scikit-learn confusion matrix üzerinden test seti (378.339 kayıt) ile üretilmiştir. Model, 1.0'lık ROC-AUC sayesinde neredeyse hiç hata yapmamıştır (yüz binde birlik hata payı). Ancak yukarıda açıklandığı üzere, bu metrikler sentetik olarak şişmiştir.

### 10. Model Gerçekten 2.522.255 Kayıt Üzerinden Mi Eğitildi?
**Evet.** Toplam `full_cleaned_dataset.parquet` satır sayısı 2.522.255'tir. Dağılım:
- Train: 1.765.578
- Validation: 378.338
- Test: 378.339

### 11. Kullanılan Feature Sayısı 79 Mu?
**Evet.** Kontrol scripti ile modelin tam olarak 79 giriş (input feature) beklediği doğrulanmıştır.

### 12. `models/full_dataset_model.joblib` Predict Yapabiliyor Mu?
**Evet.** Model dosyası `joblib.load()` ile başarıyla belleğe alınabilmiş ve veri setinden çekilen 3 satırlık örnek veri üzerinde `[0 0 0]` şeklinde doğru prediction yapabilmiştir.

## Sonuç ve "Leakage-Free" İddiası

Teknik (istatistiksel) anlamda kodlama hatasından kaynaklanan bir sızıntı (Örn: Imputer'in test setine fit edilmesi veya Target kolonunun unutulması) **YOKTUR**. Model, Scikit-Learn kurallarına %100 uygun eğitilmiştir.

Ancak **Domain spesifik (Ağ Trafiği) anlamda sızıntı VARDIR**. Random Split kullanılması, veri setinin doğası gereği "Aynı saldırının ardışık paketlerini" hem eğitime hem teste dağıtmıştır. 

Bu nedenle modelin başarısı **sentetiktir** ve gerçek dünyada (sıfırıncı gün veya farklı ağlarda) bu kadar yüksek başarı göstermesi beklenemez. Tamamen "leakage-free" (sızdırmaz) bir değerlendirme için Random Split yerine **Zaman Bazlı (Time-based split)** veya **Flow ID bazlı (GroupKFold)** bir ayrım yapılması teknik zorunluluktur.
