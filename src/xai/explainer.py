import pandas as pd
import numpy as np

class PerturbationExplainer:
    def __init__(self, model):
        self.model = model
        
    def explain(self, df_instance, top_k=3):
        '''Tekil örneklem için Naive Perturbation Importance'''
        if not hasattr(self.model, "predict_proba"):
            return []
            
        base_prob = self.model.predict_proba(df_instance)[0][1]
        importances = []
        
        for col in df_instance.columns:
            original_val = df_instance[col].iloc[0]
            
            # Değiştir (Perturb - 0'a çek)
            df_perturbed = df_instance.copy()
            df_perturbed[col] = 0.0
            
            new_prob = self.model.predict_proba(df_perturbed)[0][1]
            diff = abs(base_prob - new_prob)
            
            importances.append({"feature": col, "importance": float(diff)})
            
        importances = sorted(importances, key=lambda x: x["importance"], reverse=True)
        return importances[:top_k]
