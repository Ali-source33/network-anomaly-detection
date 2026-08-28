# Network Anomaly Detection

## Proje Özeti
Bu proje, ağ anormalliklerini makine öğrenimi (machine learning) kullanarak tespit etmeyi amaçlamaktadır. Projede CICIDS2017 veri seti kullanılmıştır.

## Problem Tanımı
Ağ trafiğindeki normal ve anormal davranışların supervised machine learning ile tespit edilmesi amaçlanmaktadır. Bu sayede olası ağ saldırıları yüksek doğrulukla yakalanabilecektir.

## Veri Seti
Projelerde **CICIDS2017** veri seti kullanılmıştır. Veri seti 8 CSV dosyasından oluşmaktadır. Raw dataset boyutu çok büyük olduğu için GitHub repository'sine dahil edilmemiştir.

## Veri İşleme
Mevcut veri işleme adımları sırasıyla şu şekildedir:
- Veri yükleme
- Temel filtreleme
- Label normalizasyonu
- Infinity değerlerinin NaN'e dönüştürülmesi
- Fwd_Bwd_Ratio oluşturulması
- Target oluşturulması
- Duplicate temizleme
- Stratified Sequential Split
- SimpleImputer
- RobustScaler
- HistGradientBoostingClassifier

Infinity değerleri NaN'e dönüştürülür. Eksik değerlerin doldurulması Pipeline içerisindeki SimpleImputer tarafından gerçekleştirilir. SimpleImputer yalnızca TRAIN verisi üzerinde fit edilir.

## Veri Bölme
Kullanılan yöntem: **Tabakalı Ardışık Bölme (Stratified Sequential Split)**
Mevcut veriler kayıt sırası korunarak aşağıdaki gibi yaklaşık olarak ayrılmıştır:
- %70 Train
- %15 Validation
- %15 Test

Bu projede GERÇEK Timestamp tabanlı chronological split yapılmamıştır. Her sınıfın sadece sıralaması korunmuştur.

## Veri Sızıntısı (Data Leakage)
Global duplicate temizleme ile birebir kayıt sızıntısı azaltılmıştır.
Preprocessing bileşenleri yalnızca TRAIN üzerinde fit edilmektedir.
Bununla birlikte güvenilir Flow ID ve Timestamp bilgisi bulunmadığından temporal/flow-level leakage tamamen dışlanamaz.

## Model Geliştirme
Değerlendirilen aday modeller şunlardır:
1. Logistic Regression
2. Random Forest
3. HistGradientBoosting

Bu modeller Validation verisi üzerinde karşılaştırılmıştır ve en iyi performansı HistGradientBoostingClassifier sağlamıştır.

## Final Model
Model: `models/final_model.joblib`
Kabul edilen feature sayısı: 79

Kullanılan Pipeline:
SimpleImputer → RobustScaler → HistGradientBoostingClassifier

**Önemli Teknik Not:** Mevcut production modeli, önceki deneysel eğitim sürecinde oluşturulmuştur. `src/train.py` dosyası daha sonra yeniden üretilebilirlik ve veri sızıntısı risklerini azaltmak amacıyla güncellenmiştir. Bu güncelleme mevcut `final_model.joblib` dosyasını değiştirmemiş veya yeniden eğitmemiştir.

## Final Performans
Bağımsız test seti üzerinde doğrulanmış performans metrikleri:
- Recall: %99.13
- Precision: %99.57
- F1 Score: %99.35
- Yanlış Pozitif (False Positive): 272
- Yanlış Negatif (False Negative): 554

## XAI
Açıklanabilir Yapay Zeka (Explainable AI - XAI) için kullanılan yöntem: **Naive Perturbation-based Feature Importance**
Bu yöntem, prediction sonrasında feature'ları pertürbe ederek tahmin olasılığındaki değişimi ölçer. Bunun yalnızca yaklaşık (approximate) bir açıklama yöntemi olduğunu ve nedensel açıklama olmadığını belirtmek gerekir.

## API
Tahmin servisi FastAPI ile sağlanmaktadır.
Endpoint: `POST /predict`
Response içinde şu alanlar bulunur:
- `prediction`: Tahmin edilen sınıf (0 veya 1)
- `probability`: Anomali olma olasılığı
- `class`: Sınıfın metinsel ifadesi (Normal / Anomaly)
- `explanation`: XAI açıklama verileri

## Dashboard
Kullanıcı arayüzü Streamlit kullanılarak geliştirilmiştir. Dashboard arayüzü kullanıcıya; tahmin, normal/anomali sonucu, probability (olasılık) ve XAI explanation (açıklama) gösterir.
Sistemde GERÇEK ZAMANLI PACKET CAPTURE YAPILMAMAKTADIR. Kullanıcı, JSON formatında özellik vektörünü göndererek tahmin sonuçlarını görüntüler.

## Canlı Ağ Trafiği ile Nasıl Kullanılır?
Proje makine öğrenimi tarafına odaklandığı için özellikleri (feature) otomatik çıkaran yerleşik bir ağ dinleyicisi içermez. Eğer kendi canlı ağ trafiğinizi (veya pcap dosyanızı) 79 satırlık bu JSON formatına dönüştürüp modeli test etmek isterseniz şu yöntemleri kullanabilirsiniz:
1. **Python ile Canlı Dinleme:** Terminal üzerinden `pip install cicflowmeter` ile Python paketini kurup, `cicflowmeter -i Wi-Fi -c trafik_sonuclari.csv` komutuyla canlı ağınızı dinleyip anında CSV'ye aktarabilirsiniz.
2. **Wireshark ile Analiz:** Bilgisayarınızdaki trafiği Wireshark ile kaydedip (`.pcap`), bu dosyayı Java tabanlı resmi **CICFlowMeter** aracına yükleyerek modelimizin beklediği 79 özelliğin otomatik hesaplanmasını sağlayabilirsiniz. Çıkan sonucu JSON formatında Dashboard'a yapıştırarak ağ trafiğinizin durumuna bakabilirsiniz.

## Kurulum
```bash
pip install -r requirements.txt
```

## Çalıştırma
Projeyi çalıştırmak için **iki ayrı terminal (komut satırı)** penceresi açmanız gerekmektedir. Projenin bulunduğu klasörde olduğunuzdan emin olduktan sonra aşağıdaki adımları izleyin.

**1. Terminal (API Sunucusu):**
```bash
# Sanal ortamı aktif edin (Windows için)
.\.venv\Scripts\activate
# veya MAC/Linux için: source .venv/bin/activate

# API'yi başlatın
uvicorn api.main:app --host 127.0.0.1 --port 8000
```

**2. Terminal (Kullanıcı Paneli / Dashboard):**
```bash
# Sanal ortamı aktif edin (Windows için)
.\.venv\Scripts\activate
# veya MAC/Linux için: source .venv/bin/activate

# Dashboard'u başlatın
streamlit run dashboard/app.py
```

## Test
Testleri çalıştırmak için:
```bash
python -m pytest tests/
```

## Sınırlamalar
- Model, CICIDS2017 veri setine sıkı sıkıya bağımlıdır.
- Gerçek zamanlı packet capture bulunmamaktadır.
- Gerçek Zero-Day detection performansının kanıtlanmamış olması.
- Modelin supervised olması.
- XAI açıklamalarının approximate (yaklaşık) olması.
- Temporal/flow-level leakage'ın tamamen dışlanamaması.

## Gelecek Çalışmalar
- Gerçek zamanlı packet capture entegrasyonu.
- Production ortamında Data drift monitoring (veri kayması izleme).
- Farklı datasetlerle cross-dataset validation (örneğin CICIDS2019, UNSW-NB15).
- Daha gelişmiş XAI yöntemleri (örneğin KernelSHAP entegrasyonu).
- Daha güçlü temporal validation teknikleri.

*Bu yaklaşım eğitimde temsil edilmeyen saldırı türlerinin oluşturduğu unseen-attack problemini azaltmayı amaçlamaktadır. Gerçek Zero-Day saldırı tespit performansı bu çalışma kapsamında kanıtlanmamıştır. Model, eğitimde temsil edilen bilinen saldırı türlerini tespit eden supervised saldırı/anomali tespit modelidir.*
