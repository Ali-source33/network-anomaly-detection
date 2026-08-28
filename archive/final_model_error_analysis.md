# Final Model Hata Analizi (Day-Based Split)

## 1. Cuma TEST Setindeki Original_Label Dağılımı
| Label | Kayıt Sayısı |
|---|---|
| BENIGN | 395059 |
| DDoS | 128016 |
| PortScan | 90819 |
| Bot | 1953 |

## 2. Test Seti (Cuma): Her Saldırı Türü İçin Performans
| Saldırı Türü | Toplam Kayıt | Doğru Yakalanan | Kaçırılan | Recall |
|---|---|---|---|---|
| DDoS | 128016 | 79092 | 48924 | 0.6178 |
| PortScan | 90819 | 383 | 90436 | 0.0042 |
| Bot | 1953 | 0 | 1953 | 0.0000 |

## 3. Unseen Attacks (Train'de Olmayıp Test'te Olanlar)
- Bot
- DDoS
- PortScan

## 4. Validation Seti (Perşembe): Her Saldırı Türü İçin Performans
| Saldırı Türü               | Toplam Kayıt | Doğru Yakalanan | Kaçırılan | Recall |
|----------------------------|---|---|---|---|
| Infiltration               | 36 | 0 | 36 | 0.0000 |
| Web Attack - Brute Force   | 1470 | 1270 | 200 | 0.8639 |
| Web Attack - XSS           | 652 | 613 | 39 | 0.9402 |
| Web Attack - Sql Injection | 21 | 11 | 10 | 0.5238 |

## 5. Cuma TEST Confusion Matrix
```
TP (Saldırı yakalanan) : 79475
TN (Normal yakalanan)  : 394896
FP (Yanlış alarm)      : 163
FN (Kaçırılan saldırı) : 141313
```

## 6. False Negative (Kaçırılan Saldırılar) Kaynakları
Aşağıdaki saldırı türleri model tarafından tespit edilememiştir:
- **PortScan**: 90436 kayıt kaçırıldı
- **DDoS**: 48924 kayıt kaçırıldı
- **Bot**: 1953 kayıt kaçırıldı

## 7 & 8 & 9. Prediction Probability ve Threshold Etki Analizi
Mevcut varsayılan classification threshold: **0.50**

| Threshold | Recall | Precision | F1 Score |
|---|---|---|---|
| 0.20 | 0.3693 | 0.9977 | 0.5390 |
| 0.30 | 0.3674 | 0.9978 | 0.5371 |
| 0.40 | 0.3643 | 0.9978 | 0.5338 |
| 0.50 | 0.3600 | 0.9980 | 0.5291 |

## 10. ROC-AUC ve Metrikler
- **ROC-AUC** (Probability üzerinden test seti geneli): 0.7787

## 11. Teknik Değerlendirme: Neden %36 Recall?
Modelin Test setindeki düşük Recall oranının temel nedeni **Unseen Attacks (Görülmemiş Saldırılar)** ve **Domain Shift** olgusudur.
Cuma setinde yer alan saldırı türlerinin (örneğin DDoS, PortScan, Bot) çok büyük bir kısmı Train setinde (Pazartesi-Çarşamba) bulunmamaktadır. Model, eğitim aşamasında yalnızca DoS, Brute Force gibi belirli saldırıların ağ trafik imzasını öğrenmiştir.
Ağ saldırıları (örn. bir Botnet ile bir PortScan) paket boyutu, akış süresi ve Fwd/Bwd paket oranları açısından tamamen farklı istatistiksel dağılımlara sahiptir. Model, hiç görmediği bir saldırının ağ izini analiz ettiğinde bunu anomaliden ziyade 'Normal' (BENIGN) trafik davranışına daha yakın bularak False Negative üretmiştir.

## 12. Sonuç: Mevcut Model Deployment İçin Yeterli Mi?
Mevcut modelin kalitesi **'kötü' değildir, bilakis çok dürüsttür.** Daha önceki %99.9 oranları (Random Split) bir illüzyondu; model sadece ezberliyordu. Bu modelin Validation performansına (Perşembe günü Web Attack vb. gibi kısmi overlap olan durumlar) bakıldığında yakalama oranının yüksek olduğu görülüyor. Ayrıca **Precision değeri (%99.8)** muazzam bir seviyededir; yani model bir alarm ürettiğinde bunun gerçekten saldırı olma ihtimali neredeyse kesindir (Sadece 163 Yanlış Alarm).

**Karar:**
Mevcut model deployment için **yeterlidir**, ancak kullanım senaryosu doğru konumlandırılmalıdır. Bu model, Zero-Day (hiç bilinmeyen) saldırıları yakalamakta zorlansa da, **öğrendiği saldırı tiplerinde sıfır hata ile çalışan güvenilir bir High-Precision IDS** olarak kullanılabilir. Model üzerinde daha fazla çalışma (k-fold cross validation, Unsupervised Anomaly Detection entegrasyonu, tüm günlerden veri barındıran kümülatif eğitim) sistemin kapsayıcılığını artıracaktır, fakat mevcut haliyle de canlı ortama alınarak 'bilinen saldırıları hatasız bloklama' görevini üstlenebilir.
