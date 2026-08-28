# Tam Veri Seti Eğitim Hazırlığı

## 1. Kullanılan CSV Dosyaları
- Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
- Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
- Friday-WorkingHours-Morning.pcap_ISCX.csv
- Monday-WorkingHours.pcap_ISCX.csv
- Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
- Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
- Tuesday-WorkingHours.pcap_ISCX.csv
- Wednesday-workingHours.pcap_ISCX.csv

## 2. Toplam Veri Boyutu
Toplam dosya sayısı: 8
Birleştirme sonrası başlangıç satır sayısı (negatif Flow Duration hariç): 2830628

## 3. Label Dağılımı
- BENIGN: 2272982
- DoS Hulk: 231073
- PortScan: 158930
- DDoS: 128027
- DoS GoldenEye: 10293
- FTP-Patator: 7938
- SSH-Patator: 5897
- DoS slowloris: 5796
- DoS Slowhttptest: 5499
- Bot: 1966
- Web Attack - Brute Force: 1507
- Web Attack - XSS: 652
- Infiltration: 36
- Web Attack - Sql Injection: 21
- Heartbleed: 11

## 4. Binary Target Dönüşümü
- BENIGN (0): 2272982
- Anomaly (1): 557646

## 5. Duplicate Analizi
Dosya içi (lokal) duplicate toplamı: 256479
Tüm veriler birleştirildikten sonraki global duplicate sayısı: 308373
Drop_duplicates() işlemi uygulanarak tüm birebir aynı satırlar temizlendi. (Not: Bu işlem data leakage riskini azaltır ancak zaman serisi sızıntısını tamamen çözdüğü iddia edilemez.)

## 6. Veri Temizleme
- Bulunan NaN sayısı: 353, tümü 0 ile dolduruldu.
- Bulunan Infinity sayısı: 2775, max finite değerlere çekildi.

## 7. Feature Engineering
Fwd_Bwd_Ratio özelliği (Total Fwd Packets / (Total Backward Packets + 1e-5)) eklendi.

## 8. Memory Optimization
Optimizasyon öncesi DataFrame boyutu: ~1593.17 MB
float64 -> float32 ve int64 -> int32 downcasting uygulandı.
Optimizasyon sonrası DataFrame boyutu: ~842.68 MB

## 9. Son Veri Yapısı
Toplam Satır Sayısı: 2522255
Özellik (Feature) Sayısı (Original_Label ve Target hariç): 79

## 10. Eğitim Öncesi Kontroller
- NaN kontrolü: Temiz
- Infinity kontrolü: Temiz
- Label kolonları: Original_Label ve Target mevcut.
- Raw CSV'ler: Değiştirilmedi.

Hazırlanan tam veri seti data/processed\full_cleaned_dataset.parquet konumuna kaydedildi.
