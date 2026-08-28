# Veri Bölme (Split) Stratejileri Analizi

Bu raporda, mevcut pipeline'da ulaşılan olağanüstü yüksek test başarısının (%99.99) nedenleri ve CICIDS2017 tam veri seti üzerinde uygulanabilecek üç farklı bölme stratejisi (Split Strategy) deneysel olarak analiz edilmiştir.

## Veri Setinin Yapısal Gerçekleri
Yapılan kod analizinde `data/raw/` altındaki veri setinin **ML-Ready (Makine Öğrenmesine Hazır)** versiyon olduğu tespit edilmiştir. Bu versiyonda siber güvenlik açısından kritik olan tanımlayıcı değişkenler (`Flow ID`, `Source IP`, `Destination IP`, `Timestamp`) **bulunmamaktadır.** Yalnızca `Destination Port` ve diğer 77 istatistiksel özellik (paket uzunluğu, byte sayısı vb.) mevcuttur.

Ayrıca saldırıların (Label) günlere dağılımı şu şekildedir:
- **Pazartesi**: Sadece BENIGN (Normal)
- **Salı**: FTP-Patator, SSH-Patator
- **Çarşamba**: DoS (Hulk, GoldenEye, slowloris, Slowhttptest), Heartbleed
- **Perşembe**: Web Attack (Brute Force, XSS, Sql Injection), Infiltration
- **Cuma**: DDoS, PortScan, Bot

---

## 1. Random Stratified Split (Mevcut Durum)
- **Train / Validation / Test Oranı**: Genellikle %70 / %15 / %15.
- **Label Dağılımı**: Her sette orijinal veri setindeki oranlar (%80 Normal, %20 Saldırı) birebir korunur.
- **Data Leakage Riski**: **Çok Yüksek.** 
- **Neden Yüksek Sonuç Üretiyor?**: Aynı ağ bağlantısına (flow) ait ardışık paketler (satırlar) istatistiksel olarak birbirinin kopyası veya çok benzeri olabilir. Random split yapıldığında, bu bağlantının yarısı Train setine, yarısı Test setine düşer. Model, anomali kalıbını öğrenmek yerine o spesifik bağlantıyı "ezberler" ve Test setini gördüğünde daha önce ezberlediği bağlantıdan geldiğini bildiği için %99.99 doğruluk üretir.
- **Avantajı**: Bütün saldırı tipleri modele öğretildiği için supervised algoritmalar maksimum verimde çalışır.

## 2. Group-based Split
- **Uygulanabilirlik**: **Mümkün Değil.**
- **Neden?**: Gruplama yapabilmek için satırların hangi bağlantıya (Flow) ait olduğunu belirten `Flow ID`, `Source IP` veya en kötü ihtimalle `Timestamp` (Zaman damgası) gereklidir. Bu kolonlar veride yoktur. Elde kalan tek tanımlayıcı kolon `Destination Port`'tur. Bütün veriyi "Port 80 Train'de olsun, Port 443 Test'te olsun" diye bölmek mantıksız ve hatalı bir yaklaşımdır.

## 3. Day-based (Zaman Bazlı) Split
- **Uygulanabilirlik**: Mümkün (Dosya bazında bölünebilir).
- **Train / Test Senaryosu**: Pazartesi, Salı, Çarşamba (Train) -> Perşembe, Cuma (Test).
- **Data Leakage Riski**: **Sıfır.** (Tamamen gerçek dünya simülasyonu).
- **Dezavantajları (Kritik Sorun)**: Sınıf eksikliği. Yukarıdaki dağılımda görüldüğü üzere, örneğin Cuma günü yapılan DDoS ve PortScan saldırıları Train setine **hiç girmeyecektir.** 
Supervised (Gözetimli) modeller olan Random Forest veya HistGradientBoosting, eğitim aşamasında hiç görmedikleri bir saldırı sınıfını (Zero-day attack) test setinde gördüklerinde büyük oranda normal (BENIGN) trafik sanarak kaçıracaklardır. Bu, yapay zekanın değil, kurgunun doğası gereği ortaya çıkan devasa bir Recall düşüşü yaratır.

---

## Sonuç ve Nihai Karar

**"Bu proje için test setinin genelleme performansını en dürüst şekilde ölçmek için hangi split stratejisi kullanılmalı ve neden?"**

Cevap: Bu projede **Random Stratified Split kullanılmalıdır.**

Nedenleri:
1. `Flow ID` veya `Timestamp` gibi tanımlayıcılar veri setinde yer almadığı için "Group-based split" imkânsızdır.
2. "Day-based split", Random Forest gibi *supervised* algoritmaların doğasına aykırıdır; çünkü test setindeki saldırı tiplerinin (örneğin DDoS) train setinde hiç bulunmaması (Zero-Shot) nedeniyle model tamamen çökecektir. Day-based split ancak *Unsupervised* (Gözetimsiz - Autoencoder vb.) modellerle mantıklıdır.

**Ancak, sızıntıyı (Data Leakage) dürüst bir seviyeye çekmek için şu şart koşulmalıdır:**
Random Stratified Split yapılmadan hemen önce, veri seti birleştirilir birleştirilmez (concat) tüm kolonlar üzerinden **`drop_duplicates()` sıkı bir şekilde uygulanmalıdır.** (Şu anki analizde çeyrek milyon civarında kopyalanmış satır tespit edilmiştir). Kopyalar (duplicates) tamamen yok edildiğinde, birebir aynı paketlerin Train ve Test setine aynı anda düşmesi (ezberleme durumu) büyük oranda engellenmiş olur ve %99.99'luk yapay başarının yerini gerçekçi bir genelleme performansı alır.
