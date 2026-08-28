# CICIDS2017 Final Model: Day-Based Split Stratejisi

CICIDS2017 veri setindeki "Flow-Level Leakage" problemini ortadan kaldırmak ve modelin "Zero-Day" (Sıfırıncı Gün) anomali tespit yeteneğini dürüst bir şekilde ölçmek amacıyla ham veri dağılımı gün bazında incelenmiş ve değerlendirilmiştir.

## 1. Ham Veri Dosya ve Gün Dağılımı

Her bir ham CSV dosyasının gün ve kayıt sayısı dağılımı aşağıdadır:

| Gün (Dosya) | Toplam Kayıt | BENIGN | Anomaly (Saldırı) | Saldırı Sınıfları ve Sayıları |
|---|---|---|---|---|
| **Pazartesi (Monday)** | 529,918 | 529,918 | 0 | - |
| **Salı (Tuesday)** | 445,909 | 432,074 | 13,835 | FTP-Patator (7,938), SSH-Patator (5,897) |
| **Çarşamba (Wednesday)** | 692,703 | 440,031 | 252,672 | DoS Hulk (231,073), DoS GoldenEye (10,293), DoS slowloris (5,796), DoS Slowhttptest (5,499), Heartbleed (11) |
| **Perşembe (Thu. Morning)** | 170,366 | 168,186 | 2,180 | Web Attack Brute Force (1,507), Web Attack XSS (652), Web Attack Sql Injection (21) |
| **Perşembe (Thu. Afternoon)**| 288,602 | 288,566 | 36 | Infiltration (36) |
| **Cuma (Fri. Morning)** | 191,033 | 189,067 | 1,966 | Bot (1,966) |
| **Cuma (Fri. Aft. PortScan)**| 286,467 | 127,537 | 158,930 | PortScan (158,930) |
| **Cuma (Fri. Aft. DDoS)** | 225,745 | 97,718 | 128,027 | DDoS (128,027) |

---

## 2. Senaryo Karşılaştırmaları

### Senaryo 1: Pazartesi-Çarşamba (TRAIN), Perşembe (VAL), Cuma (TEST)
- **TRAIN (Pzt, Sal, Çar):**
  - **Saldırı Sınıfları:** FTP-Patator, SSH-Patator, DoS (Hulk, GoldenEye, vb.), Heartbleed (7 tür).
  - **Boyutlar:** 1,668,530 Toplam | 1,402,023 Normal | 266,507 Anomaly
- **VALIDATION (Perşembe):**
  - **Saldırı Sınıfları:** Web Attacks, Infiltration (4 tür).
  - **Boyutlar:** 458,968 Toplam | 456,752 Normal | 2,216 Anomaly
- **TEST (Cuma):**
  - **Saldırı Sınıfları:** Bot, PortScan, DDoS (3 tür).
  - **Boyutlar:** 703,245 Toplam | 414,322 Normal | 288,923 Anomaly

* **Overlap Oranı:** %0 (Hiçbir saldırı türü iki kümede aynı anda bulunmaz).
* **Değerlendirme:** Harika bir ayrım. Model kaba kuvvet (Patator) ve hacimli (DoS) saldırıları öğrenir; Validation'da çok sinsi ve gizli (Infiltration, Web) saldırılara karşı sınanır; Test'te ise yepyeni bir hacimli saldırı (DDoS) ve tarama (PortScan) tipleriyle karşılaşır.

### Senaryo 2: Pazartesi-Perşembe (TRAIN), Cuma (TEST)
- **TRAIN (Pzt-Perş):**
  - **Saldırı Sınıfları:** Patator, DoS, Web Attacks, Infiltration (11 tür).
  - **Boyutlar:** 2,127,498 Toplam | 1,858,775 Normal | 268,723 Anomaly
- **TEST (Cuma):**
  - **Saldırı Sınıfları:** Bot, PortScan, DDoS (3 tür).
  - **Boyutlar:** 703,245 Toplam | 414,322 Normal | 288,923 Anomaly

* **Overlap Oranı:** %0
* **Değerlendirme:** Validation kümesi eksiktir. Veriyi 3'e bölmek için Cuma gününün içindeki dosyaları (örneğin Cuma sabahı Validation, Cuma öğleden sonra Test) ayırmak gerekir, bu da dosya/gün bazlı saflığı bozar.

---

## 3. "Binary Anomaly Detection" Açısından Unseen Attacks (Görülmemiş Saldırılar)

Bir anomali tespit (anomaly detection) sisteminin amacı, belirli bir saldırı türünün imzasını ezberlemek değil, **Normal (BENIGN) ağ trafiği davranışının sınırlarını öğrenmek** ve bu sınırların dışına çıkan her şeyi (daha önce görsün veya görmesin) **Saldırı (Anomaly = 1)** olarak işaretleyebilmektir.

Test setindeki bir saldırı türünün Train setinde hiç bulunmaması (Zero-Day senaryosu), binary anomaly detection açısından **modelin gerçek hayattaki başarısının en dürüst testidir.** Eğer model, sadece Train'de gördüğü DoS saldırılarını yakalayıp, Test'teki DDoS veya Web Saldırılarını `Normal` olarak sınıflandırıyorsa, bu model aslında bir *Anomaly Detector* değil, sadece bir *DoS Detector* (imza tabanlı ezberci) olmuş demektir.

Gün bazlı ayrım (Day-Based Split) ile Leakage tamamen sıfırlanır ve modelin gerçekten Normal veriyi anlayıp anlamadığı test edilir.

---

## 4. Nihai Öneri Kararı

Mevcut bulgular ve siber güvenlik makine öğrenimi pratikleri (Zero-Day Test) ışığında:

**Final model için şu günler TRAIN, şu gün VALIDATION, şu gün TEST kullanılmalıdır:**

*   **TRAIN:** Pazartesi, Salı, Çarşamba (Monday, Tuesday, Wednesday)
*   **VALIDATION:** Perşembe (Thursday)
*   **TEST:** Cuma (Friday)

### Teknik Nedenler:
1. **Veri Sızıntısının (Data Leakage) Önlenmesi:** CICIDS2017'de aynı akışa (Flow) ait paketlerin Train ve Test'e rastgele sızması (ROC-AUC'nin %100 çıkma nedeni) günlerin ayrılmasıyla fiziksel olarak engellenir. Pazartesi yapılan bir bağlantı, Cuma günü tekrar edilmemektedir.
2. **Sıfırıncı Gün (Zero-Day) Simülasyonu:** Validation (Perşembe) ve Test (Cuma) kümelerinde bulunan toplam 7 saldırı tipinin hiçbiri Train setinde yoktur. Modeli en zorlu ve en gerçekçi koşulda değerlendirir.
3. **Hiperparametre ve Model Seçimi İçin İdeal Validation:** Perşembe günü ağırlıklı olarak sinsi (stealthy) Infiltration ve Web saldırıları içerir. Bu gizli anomalileri yakalayabilen hiperparametreleri (Validation Tuning) bulmak, modelin kalitesini çok artırır. Son olarak devasa DDoS ve PortScan (Cuma) ile son nihai (Test) kararı verilir.
