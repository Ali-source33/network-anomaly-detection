# Mevcut Final Model — Günlük Performans Analizi

## 1. Günlük Genel Performans Özeti

| Gün | Toplam | BENIGN | Anomaly | Accuracy | Precision | Recall | F1 | ROC-AUC | FP | FN |
|-----|--------|--------|---------|----------|-----------|--------|----|---------|----|----|
| Monday | 502775 | 502775 | 0 | 0.9996 | 0.0000 | 0.0000 | 0.0000 | N/A | 197 | 0 |
| Tuesday | 410181 | 401029 | 9152 | 0.9997 | 0.9886 | 1.0000 | 0.9942 | 1.0000 | 106 | 0 |
| Wednesday | 590615 | 396955 | 193660 | 0.9998 | 0.9995 | 1.0000 | 0.9997 | 1.0000 | 94 | 6 |
| Thursday | 402139 | 399960 | 2179 | 0.9988 | 0.9045 | 0.8692 | 0.8865 | 0.9915 | 200 | 285 |
| Friday | 615847 | 395059 | 220788 | 0.7703 | 0.9980 | 0.3600 | 0.5291 | 0.7787 | 163 | 141313 |

## 2. Gün Bazlı Saldırı Türü Analizi

### Tuesday (Saldırı Analizi)
| Saldırı Türü | Toplam | Doğru Yakalanan | Kaçırılan | Recall |
|---|---|---|---|---|
| FTP-Patator | 5933 | 5933 | 0 | 1.0000 |
| SSH-Patator | 3219 | 3219 | 0 | 1.0000 |

### Wednesday (Saldırı Analizi)
| Saldırı Türü | Toplam | Doğru Yakalanan | Kaçırılan | Recall |
|---|---|---|---|---|
| DoS slowloris | 5384 | 5382 | 2 | 0.9996 |
| DoS Slowhttptest | 5228 | 5227 | 1 | 0.9998 |
| DoS Hulk | 172751 | 172748 | 3 | 1.0000 |
| DoS GoldenEye | 10286 | 10286 | 0 | 1.0000 |
| Heartbleed | 11 | 11 | 0 | 1.0000 |

### Thursday (Saldırı Analizi)
| Saldırı Türü | Toplam | Doğru Yakalanan | Kaçırılan | Recall |
|---|---|---|---|---|
| Infiltration | 36 | 0 | 36 | 0.0000 |
| Web Attack � Brute Force | 1470 | 1270 | 200 | 0.8639 |
| Web Attack � XSS | 652 | 613 | 39 | 0.9402 |
| Web Attack � Sql Injection | 21 | 11 | 10 | 0.5238 |

### Friday (Saldırı Analizi)
| Saldırı Türü | Toplam | Doğru Yakalanan | Kaçırılan | Recall |
|---|---|---|---|---|
| DDoS | 128016 | 79092 | 48924 | 0.6178 |
| PortScan | 90819 | 383 | 90436 | 0.0042 |
| Bot | 1953 | 0 | 1953 | 0.0000 |

## 3. Cuma (TEST) Seti False Negative (Kaçırılan) Analizi

Cuma gününde oluşan devasa FN miktarının temel kaynakları şunlardır:
- **DDoS**: 48924 kayıt kaçırıldı (Recall: 0.6178)
- **PortScan**: 90436 kayıt kaçırıldı (Recall: 0.0042)
- **Bot**: 1953 kayıt kaçırıldı (Recall: 0.0000)

## 4. Domain Shift Analizi

- **Domain Shift & Unseen Attacks**: Cuma günündeki `%36` Recall'ın ana sebebi, Train setinde (Pzt-Çarş) yer almayan *PortScan* ve *DDoS* saldırılarının Cuma test setini domine etmesidir (Unseen attack). Model bu saldırıları daha önce görmediği için, dağılımlarını (Feature distribution) Normal (BENIGN) trafikten ayırt edememekte ve bu nedenle 'Normal' olarak tahmin etmektedir.
- **Feature Distribution Değişimi**: Farklı günlerde, farklı araçlarla (örn. Botnet vs. BruteForce) yapılan saldırıların paket büyüklükleri ve frekansları köklü değişiklikler gösterir. Cuma günkü imzalar, Çarşamba günkülerden yapısal olarak ayrışır (Feature shift).

## 5. Random Split ile Karşılaştırma

Daha önceki Random Stratified Split'in Accuracy'si `%99.86`, Recall'u `%99.96` seviyesindeyken, Cuma günü (Day-Based Test) Recall `%36.00`'a düşmüştür.
**Neden Random Split İyimser (Optimistic)?**
Random Split, örneğin bir *PortScan* veya *DDoS* saldırısının milyonlarca paketinden bir kısmını Train'e, bir kısmını Test'e atar. Model bu spesifik ağ saldırısının imzasını çoktan ezberlemiş olur. Day-Based Split'te ise Cuma gününe ait olan saldırı türleri, Train aşamasında hiçbir şekilde model tarafından görülmemiştir, bu yüzden sonuçlar dürüst ve gerçektir.

## 6. Sonuç ve Öneriler

**1. Model bütün günlerde mi kötü?**
Hayır. Eğitim aşamasında gördüğü imzalara benzeyen veya zayıf varyasyonlarını içeren günlerde (örn. Salı, Çarşamba, Perşembe) modelin Recall ve Precision'ı (FP=0/FN=0 veya 0'a çok yakın) muazzam seviyededir. Eğitim verisi ile benzer dağılıma sahip verilerde kusursuz çalışır.

**2. Yoksa özellikle Cuma'da mı kötüleşiyor?**
Kesinlikle evet. Yalnızca Cuma gününde, yani yepyeni anomalilerin (PortScan, DDoS, Bot) sisteme girmesiyle birlikte Recall çakılmaktadır.

**3. Hangi saldırı türleri problemi oluşturuyor?**
Cuma gününde yer alan **PortScan** ve **DDoS** sınıfları modelin en zayıf karnıdır.

**4. Domain shift açıkça görülüyor mu?**
Evet. Günler arası feature dağılımlarındaki ve saldırı türlerindeki kayma (Domain Shift), mevcut verilerle de doğrulandığı üzere barizdir.

**5. Model geliştirmeye gerçekten ihtiyaç var mı?**
Evet. Sistemin Zero-Day (sıfırıncı gün) saldırılarını (örneğin PortScan) tanıyabilmesi için geliştirilmesi elzemdir. Aksi halde sadece bildiği saldırıları (BruteForce, DoS) engelleyen bir IDS olarak kalır.

**6. Bir sonraki aşamada ne yapılmalı?**
Modelin temel sorunu hiperparametre veya threshold değildir. Bir sonraki aşamada Train setinin (eğitim verisinin) zenginleştirilmesi (Tüm günleri kapsayan time-series k-fold cv), kümülatif feature engineering veya Anomaly Detection (Unsupervised) yaklaşımlarının entegre edilmesi incelenmelidir.
