import os
import glob
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import joblib

def main():
    # Veri Yükleme
    print("Veri Yükleme başlatılıyor...")
    raw_dir = "data/raw"
    csv_files = sorted(glob.glob(os.path.join(raw_dir, "*.csv")))
    
    df_list = []
    for f in csv_files:
        df_chunk = pd.read_csv(f, low_memory=False)
        df_chunk.columns = df_chunk.columns.str.strip()
        
        # Hatalı "Flow Duration" filtrelemesi
        if 'Flow Duration' in df_chunk.columns:
            df_chunk = df_chunk[df_chunk['Flow Duration'] >= 0]
            
        df_list.append(df_chunk)
        
    df = pd.concat(df_list, ignore_index=True)
    del df_list
    
    # Veri Temizleme
    print("Veri Temizleme yapılıyor...")
    df.rename(columns={'Label': 'Original_Label'}, inplace=True)
    
    # NaN ve Infinity İşlemleri
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
                
    # Feature Engineering
    print("Feature Engineering yapılıyor...")
    if 'Total Fwd Packets' in df.columns and 'Total Backward Packets' in df.columns:
        df['Fwd_Bwd_Ratio'] = df['Total Fwd Packets'] / (df['Total Backward Packets'] + 1e-5)
        
    df['Target'] = (df['Original_Label'] != 'BENIGN').astype(int)
    
    # Duplicate Temizleme
    dupe_subset = [c for c in df.columns if c not in ['Target', 'Original_Label']]
    df_dedup = df.drop_duplicates(subset=dupe_subset, keep='first')
    
    # Veri Bölme
    print("Veri Bölme işlemi gerçekleştiriliyor...")
    train_list, val_list, test_list = [], [], []
    
    for label in df_dedup['Original_Label'].unique():
        sub = df_dedup[df_dedup['Original_Label'] == label].copy()
        n = len(sub)
        n_train = int(n * 0.70)
        n_val = int(n * 0.15)
        
        train_list.append(sub.iloc[:n_train])
        val_list.append(sub.iloc[n_train:n_train+n_val])
        test_list.append(sub.iloc[n_train+n_val:])
        
    train_df = pd.concat(train_list)
    val_df = pd.concat(val_list)
    test_df = pd.concat(test_list)
    
    X_train = train_df.drop(columns=['Target', 'Original_Label'])
    y_train = train_df['Target']
    
    X_val = val_df.drop(columns=['Target', 'Original_Label'])
    y_val = val_df['Target']
    
    X_test = test_df.drop(columns=['Target', 'Original_Label'])
    y_test = test_df['Target']
    
    # 79 Feature olduğunu doğrula
    print(f"Feature Sayısı: {X_train.shape[1]}")
    
    # Preprocessing
    print("Preprocessing ve Model Eğitimi hazırlanıyor...")
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', RobustScaler()),
        ('classifier', HistGradientBoostingClassifier(class_weight='balanced', random_state=42))
    ])
    
    # Model Eğitimi
    # DİKKAT: Eğitim sürecini doğrulamak için tasarlandığından varsayılan olarak eğitim pas geçilmiştir.
    # Eğitimi başlatmak için aşağıdaki yorum satırlarını kaldırın.
    '''
    print("Model Eğitimi başlatılıyor (HistGradientBoostingClassifier)...")
    pipeline.fit(X_train, y_train)
    
    # Değerlendirme
    print("Değerlendirme (Validation) yapılıyor...")
    val_preds = pipeline.predict(X_val)
    val_probs = pipeline.predict_proba(X_val)[:, 1]
    
    print(f"Validation Recall: {recall_score(y_val, val_preds):.4f}")
    print(f"Validation Precision: {precision_score(y_val, val_preds):.4f}")
    print(f"Validation ROC-AUC: {roc_auc_score(y_val, val_probs):.4f}")
    
    # Model Kaydetme
    # Mevcut final_model.joblib üzerine yazılmaması için deneysel adla kaydedilir.
    output_model = "models/reproducible_model.joblib"
    joblib.dump(pipeline, output_model)
    print(f"Model başarıyla {output_model} konumuna kaydedildi.")
    '''
    print("Script başarılı. Final production model üzerine yazılmadı.")

if __name__ == '__main__':
    main()
