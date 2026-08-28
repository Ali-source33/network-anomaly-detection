# Final Temizlik Envanteri

Bu rapor, projedeki tüm dosyaların sınıflandırılmasını ve final temizlik öncesi hangi dosyaların güvenle silinebileceğini göstermektedir.

## 1. Modeller (`models/`)
| Dosya Adı | Ne İşe Yarıyor? | Production İçin Gerekli Mi? | Silinebilir Mi? | Notlar |
|-----------|-----------------|-----------------------------|-----------------|--------|
| `final_model.joblib` | Nihai üretim modeli (API/Dashboard kullanır). | **EVET** | **HAYIR** | Dokunulmamalıdır. |
| `experimental_model.joblib` | Deneysel süreçte üretilen model. (Artık final_model olarak kopyalandı). | HAYIR | **EVET** | Kopyası production'a alındığı için silinebilir. |
| `final_model_backup_before_final.joblib` | Hatalı (Day-Based) modelin yedeği. | HAYIR | **EVET (veya Arşiv)** | Eski hatalı modele dönüş için tutulabilir, ancak gereksizdir. |
| `final_model_new.joblib` | Eski deneylerden kalma geçici model. | HAYIR | **EVET** | Güvenle silinebilir. |
| `final_model_backup.joblib` | Çok daha eski bir yedek. | HAYIR | **EVET** | Güvenle silinebilir. |
| `full_dataset_model.joblib` | İlk full dataset denemesinde oluşturulmuş eski model. | HAYIR | **EVET** | Güvenle silinebilir. |

## 2. API ve Dashboard (`api/`, `dashboard/`)
| Dosya Adı | Ne İşe Yarıyor? | Production İçin Gerekli Mi? | Silinebilir Mi? |
|-----------|-----------------|-----------------------------|-----------------|
| `api/main.py` | FastAPI arka uç servisi. Modeli sunar. | **EVET** | **HAYIR** |
| `dashboard/app.py` | Streamlit ön yüz arayüzü. Tahminleri gösterir. | **EVET** | **HAYIR** |

## 3. Kaynak Kod ve Testler (`src/`, `tests/`)
| Dosya Adı | Ne İşe Yarıyor? | Production İçin Gerekli Mi? | Silinebilir Mi? |
|-----------|-----------------|-----------------------------|-----------------|
| `tests/test_pipeline.py` | API ve test pipeline mantığı. | **EVET** | **HAYIR** |
| `src/pipeline.py` | Eski (veya standart) eğitim pipeline taslağı. | HAYIR | **EVET** |
| `src/day_based_pipeline.py` | Hatalı modelin eğitim kodu. | HAYIR | **EVET** |
| `src/full_dataset_pipeline.py` | Eski eğitim deneme scripti. | HAYIR | **EVET** |
| `src/preprocessing/clean_data.py` | Veri temizleme taslağı (Kullanılmıyor). | HAYIR | **EVET** |
| `src/test_environment.py` | Ortam test scripti. | HAYIR | **EVET** |

> **Not:** Eğitim tamamlandığı ve `final_model.joblib` üretimde olduğu için `src/` altındaki pipeline dosyalarına aktif olarak ihtiyaç yoktur. İleride tekrar model eğitilecekse tek ve temiz bir `train.py` dosyasına dönüştürülmelidir.

## 4. Geçici Dosyalar (`scratch/`)
| Klasör / İçerik | Ne İşe Yarıyor? | Production İçin Gerekli Mi? | Silinebilir Mi? |
|-----------------|-----------------|-----------------------------|-----------------|
| `scratch/*.py`, `*.json` | Deneyler, doğrulama testleri ve analiz betikleri. | HAYIR | **EVET** |

Tamamı proje geliştirme aşamasında oluşturulmuş tek seferlik betiklerdir. Tamamı silinebilir.

## 5. Veri Klasörleri (`data/raw/`, `data/processed/`)
| Klasör / İçerik | Ne İşe Yarıyor? | Production İçin Gerekli Mi? | Silinebilir Mi? |
|-----------------|-----------------|-----------------------------|-----------------|
| `data/raw/*.csv` | Orijinal indirilen veri seti dosyaları. | HAYIR (Eğitim bitti) | **HAYIR (Dokunma)** |
| `data/processed/full_cleaned_dataset.parquet` | Ara temizlenmiş veri seti. | HAYIR | **EVET** |
| `data/processed/split_indices.npz` | Geçici indeks yedeği. | HAYIR | **EVET** |
| Diğer `processed` .csv dosyaları | Eski işlemlerden kalma çöpler. | HAYIR | **EVET** |

## 6. Raporlar (`reports/`)
| Kategori | Dosyalar | Silinebilir Mi? | Notlar |
|----------|----------|-----------------|--------|
| **Final Dokümantasyon** | `experimental_model_validation.md`, `model_improvement_experiment.md` | **HAYIR** | Projenin güncel başarılı durumunu açıklar. |
| **Gereksiz/Eski Raporlar** | `daily_performance_analysis.md`, `final_model_error_analysis.md`, `split_strategy_analysis.md`, ve benzeri tüm deney raporları. | **EVET** | Projenin geçmiş evrelerindeki problemlerini anlatır, model başarıya ulaştığı için artık gereksizdir. |
