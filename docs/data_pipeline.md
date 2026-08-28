# Veri Boru Hattı (Data Pipeline)

**Veri Kaynağı:** CICIDS2017 Veri Seti (8 CSV)

**Doğru Akış:**

Raw CICIDS2017  
↓  
Temel filtreleme  
↓  
Label normalizasyonu  
↓  
Infinity → NaN  
↓  
Fwd_Bwd_Ratio  
↓  
Target  
↓  
Duplicate temizleme  
↓  
Stratified Sequential Split  
↓  
TRAIN üzerinde SimpleImputer.fit  
↓  
TRAIN üzerinde RobustScaler.fit  
↓  
HistGradientBoostingClassifier  

Validation ve Test için preprocessing yalnızca transform olarak uygulanır.
