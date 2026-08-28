# Veri Seti Dağılımı ve Değerlendirme (Split) Stratejileri Analizi

Bu raporda CICIDS2017 veri setinin ham CSV dosyaları incelenmiş, saldırıların günlere dağılımı çıkarılmış ve farklı veri bölme (split) stratejilerinin modelin genelleme performansına etkileri deneysel olarak analiz edilmiştir. 

## 1. Ham Veri Seti Gün ve Saldırı Dağılımı

Tüm CSV'ler incelendiğinde her dosyanın (ve günün) spesifik saldırı türlerini barındırdığı görülmektedir:

| Dosya (Gün) | Toplam Kayıt | BENIGN (Normal) | Saldırı Türleri ve Sayıları |
|---|---|---|---|
| **Monday** | 529,918 | 529,918 | *(Saldırı Yok)* |
| **Tuesday** | 445,909 | 432,074 | FTP-Patator (7,938), SSH-Patator (5,897) |
| **Wednesday** | 692,703 | 440,031 | DoS Hulk (231,073), DoS GoldenEye (10,293), DoS slowloris (5,796), DoS Slowhttptest (5,499), Heartbleed (11) |
| **Thursday Morning** | 170,366 | 168,186 | Web Attack Brute Force (1,507), Web Attack XSS (652), Web Attack Sql Injection (21) |
| **Thursday Afternoon** | 288,602 | 288,566 | Infiltration (36) |
| **Friday Morning** | 191,033 | 189,067 | Bot (1,966) |
| **Friday Afternoon (PortScan)** | 286,467 | 127,537 | PortScan (158,930) |
| **Friday Afternoon (DDoS)** | 225,745 | 97,718 | DDoS (128,027) |

## 2. Split (Veri Bölme) Stratejilerinin Analizi

Siber güvenlik veri setlerinde verinin nasıl bölündüğü, modelin gerçek başarısını doğrudan belirler. Aşağıda 3 farklı strateji analiz edilmiştir.

### Strateji 1: Random Stratified Split (Mevcut Yöntem)
- **Mantığı:** Tüm dosyalar birleştirilir ve rastgele (örneğin %70 Train, %30 Test) bölünür.
- **Overlap (Kesişim) Oranı:** %100. Train setinde olan 15 saldırı türünün tamamı Test setinde de bulunur.
- **Domain Leakage (Sızıntı) Sorunu:** Siber saldırılar "ağ akışları (flow)" şeklindedir ve saniyeler içinde binlerce benzer paket/satır üretir. Rastgele bölme yapıldığında, **Aynı saldırı akışına ait paketlerin yarısı Train'e, diğer yarısı Test'e düşer**.
- **Sonuç:** Model siber güvenliğin mantığını veya anomaliyi öğrenmez; sadece ezber (memorization) yapar. Orijinal modeldeki `ROC-AUC = 1.0000` çıkmasının yegane sebebi budur. Test seti, Train setinin neredeyse birebir kopyası haline gelmiştir.

### Strateji 2: Group Split (Ağ Akışı Bazlı Bölme)
- **Mantığı:** `Flow ID` veya `Source IP` + `Timestamp` kullanılarak, aynı ağ oturumuna ait tüm satırlar gruplanır ve gruplar bölünür (GroupKFold). Böylece bir akışın yarısı Train'de, yarısı Test'te olamaz.
- **Uygulanabilirlik Analizi:** **UYGULANAMAZ.**
- **Neden?** `data/raw/*.csv` dosyalarının taraması sonucunda `Flow ID`, `Source IP`, `Destination IP` ve `Timestamp` kolonlarının raw dataset'ten silinmiş olduğu tespit edilmiştir. İlgili kolonlar mevcut olmadığı için matematiksel olarak satırları akış bazında gruplamak imkansızdır.

### Strateji 3: Dosya / Gün Bazlı Split (Day-Based Split)
- **Mantığı:** Model belirli günlerde (Örn: Pazartesi, Salı, Çarşamba) eğitilir, daha önce hiç görmediği günlerde (Perşembe, Cuma) test edilir.
- **Overlap (Kesişim) Oranı:** **%0 (Sıfır)**. Her gün tamamen farklı saldırı vektörleri içerdiği için, Train ve Test setlerindeki saldırı tipleri hiçbir şekilde kesişmez.
- **Unseen Attacks (Görülmemiş Saldırılar):** Eğitimi Pzt-Çarşamba yaparsak; Test setindeki *Web Attacks, Infiltration, Bot, PortScan ve DDoS* saldırılarının tamamı **Zero-Day (Sıfırıncı Gün)** saldırısı muamelesi görür.
- **Sonuç:** Bu strateji veri sızıntısını (leakage) tamamen engeller. Ancak Random Forest veya HistGradientBoosting gibi gözetimli (supervised) ağaç modelleri, daha önce imzasını (feature yapısını) hiç görmedikleri yepyeni bir saldırı türünü tanımakta çok zorlanacakları için metrikler (Accuracy, Recall) dramatik şekilde düşecektir.

## 3. Genel Değerlendirme

Mevcut CICIDS2017 `MachineLearningCSV` versiyonu (IP ve FlowID bilgileri içermeyen versiyon), Gözetimli Öğrenme (Supervised Learning) ile anomali tespiti yapmak için ciddi bir çıkmaz (trade-off) sunmaktadır:

1. **Random Split kullanırsak:** Metrikler %99.99 çıkar, ancak gerçek dünyayı yansıtmaz (Data Leakage).
2. **Gün bazlı (Day-based) Split kullanırsak:** Leakage sıfırlanır, ancak model test setindeki saldırıları daha önce hiç görmediği için (Zero-day) denetimli öğrenme algoritmaları sınıfta kalır; anomali tespiti (örneğin One-Class SVM veya Autoencoder) yaklaşımlarına geçilmesi gerekir.

Pipeline veya model değiştirilmemiştir, mevcut yapı matematiksel olarak başarılı olsa da siber güvenlik domaini açısından bu teknik kısıtlamalar dikkate alınmalıdır.
