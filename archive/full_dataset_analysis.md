# CICIDS2017 Tam Veri Seti Analizi

## 1. Bulunan Dosyalar
`data/raw/` dizininde toplam **8 adet** CSV dosyası tespit edilmiştir:
1. `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`
2. `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`
3. `Friday-WorkingHours-Morning.pcap_ISCX.csv`
4. `Monday-WorkingHours.pcap_ISCX.csv`
5. `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv`
6. `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv`
7. `Tuesday-WorkingHours.pcap_ISCX.csv`
8. `Wednesday-workingHours.pcap_ISCX.csv`

## 2. Dosya Boyutları
- **Toplam Satır Sayısı**: 2.830.743
- **Toplam Kolon Sayısı**: 79
- **RAM Ayak İzi (Memory Footprint)**: Sadece raw verilerin pandas ile yüklenmiş hali yaklaşık **1.72 GB** tutmaktadır.

## 3. Kolon Uyumluluğu
Yapılan analizde, sütun isimlerinin etrafındaki boşluklar (whitespace) temizlendiğinde, 8 dosyanın da kolon isimlerinin, sırasının ve sayısının (79 kolon) **%100 uyumlu** olduğu doğrulanmıştır. Herhangi bir yapısal farklılık yoktur.

## 4. Label Dağılımları
Veri setinde BENIGN (Normal) trafik dahil toplam **15 farklı Label** bulunmaktadır:
- **BENIGN**: 2.273.097 (%80.30)
- **DoS Hulk**: 231.073 (%8.16)
- **PortScan**: 158.930 (%5.61)
- **DDoS**: 128.027 (%4.52)
- **DoS GoldenEye**: 10.293
- **FTP-Patator**: 7.938
- **SSH-Patator**: 5.897
- **DoS slowloris**: 5.796
- **DoS Slowhttptest**: 5.499
- **Bot**: 1.966
- **Web Attack - Brute Force**: 1.507
- **Web Attack - XSS**: 652
- **Infiltration**: 36
- **Web Attack - Sql Injection**: 21
- **Heartbleed**: 11

## 5. Veri Kalitesi
Tüm veri seti genelinde:
- **Eksik Veri (NaN)**: 1.358 hücre
- **Sonsuz Veri (Infinity)**: 4.376 hücre
- **Negatif Flow Duration**: 115 satır
- **Kopya (Duplicate) Kayıtlar**: 256.479 satır
Bu hatalı kayıtlar, mevcut temizleme mantığı ile (NaN'ların 0 yapılması, Infinity'lerin max değere çekilmesi, negatif Flow Duration'ların ve kopyaların silinmesi) rahatlıkla çözülebilecek durumdadır.

## 6. Bellek Kullanımı
Pandas ile tüm CSV dosyaları aynı anda DataFrame'e yüklendiğinde ve `concat` edildiğinde bellek kullanımı 1.72 GB'den başlar, ancak preprocessing (ölçekleme, train_test_split vb.) işlemleri sırasında kopyalar oluşturulacağı için RAM tüketimi **6-8 GB** seviyelerine çıkabilir. Standart bir sistem için sınırdadır, bu nedenle 64-bit float'ların 32-bit float'lara indirgenmesi (downcasting) büyük ölçüde rahatlatacaktır. `PySpark` veya `Polars`'a henüz gerek yoktur; pandas `dtype` optimizasyonu ile çözülebilir.

## 7. Cleaning Stratejisi
Mevcut pipeline'daki temizleme stratejisi (eksik/sonsuz/negatif değerlerin ayıklanması) 8 dosya için de birebir geçerlidir ve teknik olarak doğrudur. Tek fark, dosyalar tek tek `clean_data.py` ile işlendikten sonra dosya içi kopyalar (intra-file duplicates) silinmektedir. Ancak dosyalar arası kopyaları (cross-file duplicates) yakalamak için pipeline'ın eğitim öncesi birleştirdiği aşamada (concatenation sonrası) son bir `drop_duplicates()` atması gerekebilir.

## 8. Data Split Stratejisi
Random Stratified Split yöntemi, verinin her Label oranını koruduğu için teoride iyidir ancak **zamansal ağ trafiği (network flows) için yüksek sızıntı riski taşır.** 
Özellikle ağ verilerinde aynı bağlantıya (flow) ait paketler birbirine aşırı benzer veya aynı özelliklere sahip olabilir. Random split yapıldığında bu benzer satırların bir kısmı Train'e, bir kısmı Test'e düşer. Model, anomali kalıbını (pattern) öğrenmek yerine o spesifik bağlantıyı ezberler, bu da %99.99 gibi olağanüstü yüksek ama yanıltıcı bir doğruluk oranına neden olur.

## 9. Data Leakage Riskleri
Mevcut çok yüksek Accuracy ve F1 skorlarının temel sebebi yukarıda bahsedilen "Flow-level Data Leakage" (Akış bazlı veri sızıntısı) sorunudur. Ağır sızıntıyı engellemek için:
- **Group-based Split**: Aynı Kaynak/Hedef IP (Source/Destination IP) veya Akış ID'sine (Flow ID) sahip olan kayıtlar ya tamamen Train setine ya da tamamen Test setine düşecek şekilde gruplandırılarak (`GroupShuffleSplit`) bölünmelidir. Ancak bu kolonlar çıkarılmışsa, **Time-based (Day-based)** split (Örneğin Pazartesi-Perşembe Train, Cuma Test) uygulanmalıdır. (Fakat CICIDS2017'de bazı saldırılar sadece spesifik günlerde yapılmıştır, bu yüzden Time-based split yapıldığında test setinde görülmeyen veya train'de öğretilmeyen saldırı sınıfları ortaya çıkacaktır).

## 10. Önerilen Eğitim Pipeline'ı
1. **Cleaning**: `clean_data.py`, `data/raw/` altındaki tüm 8 CSV'yi sırayla okuyup, kolon isimlerini normalize ederek, temel NaN/Inf/Negatif temizliğini yapıp `data/processed/` altına kaydetmeli.
2. **Loading & Memory**: `pipeline.py` bu 8 dosyayı birleştirirken (concat) doğrudan `float32` ve `int32` downcasting yapmalı.
3. **Splitting**: Random split yerine sızıntıyı kesecek Group tabanlı bir split yapısı veya sızıntı kabullenilerek %100 duplicate kontrolünden geçen sıkı bir Random Split uygulanmalı. 
4. **Modeling**: Model yapısı korunarak tüm veri seti üzerinden eğitilmeli.
