# Tam Veri Seti Train / Validation / Test Ayrımı

## 1. Veri Seti
Kullanılan dosya: `data/processed/full_cleaned_dataset.parquet`
Toplam satır sayısı: 2522255

## 2. Split Oranları
- Train: %70
- Validation: %15
- Test: %15
- Kullanılan random_state: 42

## 3. Train Dağılımı
- Toplam Satır: 1765578
- Normal (BENIGN): 1467463 (%83.12)
- Anomaly (Saldırı): 298115 (%16.88)

## 4. Validation Dağılımı
- Toplam Satır: 378338
- Normal (BENIGN): 314457 (%83.12)
- Anomaly (Saldırı): 63881 (%16.88)

## 5. Test Dağılımı
- Toplam Satır: 378339
- Normal (BENIGN): 314457 (%83.12)
- Anomaly (Saldırı): 63882 (%16.88)

## 6. Leakage Kontrolü
- Train ve Validation kesişimi: 0 kayıt
- Train ve Test kesişimi: 0 kayıt
- Validation ve Test kesişimi: 0 kayıt
- Sonuç: Kesişen veya sızan hiçbir kayıt yoktur. Veri seti öncesinde kopyalardan arındırıldığı için birebir aynı kayıtların sızma (ezberletme) riski ortadan kaldırılmıştır.

## 7. Bellek Kullanımı
- Bölünen verileri 3 farklı gigabaytlık dosya olarak kaydetmek yerine, yalnızca indeks numaraları (`split_indices.npz`) olarak RAM ve disk tasarrufu yapacak şekilde kaydedilmiştir.
- Model eğitimi aşamasında orijinal dataset yüklenip bu indeks numaraları çağırılarak bellek şişmesi engellenecektir.

## 8. Sonraki Aşama
- Veri hazırlığı ve split işlemi başarıyla bitmiştir. Artık `src/pipeline.py` modülü veya yeni bir script üzerinden, Train seti kullanılarak Preprocessing (Scaling, Imputation vb.) adımları uygulanabilir ve model eğitimine geçilebilir.
