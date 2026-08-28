# Modeller (Models)

`final_model.joblib`:
- Serialize edilmiş (binary) model dosyasıdır.
- HistGradientBoostingClassifier pipeline'ı içerir.
- 79 feature kabul eder.
- Production API tarafından doğrudan kullanılır.
- Text editörü ile okunabilir bir kaynak kod dosyası (source code) değildir.

Modelin eğitim kodu `src/train.py` dosyasıdır. Eğitim scriptinin mevcut haliyle otomatik olarak production modelini değiştirmediğini, `final_model.joblib`'in production modeli olduğunu belirtmek gerekir. `src/train.py` bir "Reproducibility-oriented training script"tir.
