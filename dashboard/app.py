import streamlit as st
import requests
import pandas as pd
import json
import os

st.set_page_config(page_title="Network Anomaly Detection", layout="wide", initial_sidebar_state="expanded")

# -- CSS INJECTION --
st.markdown("""
<style>
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700;900&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
    }

    /* Main App Background */
    .stApp {
        background-color: #0A0A0B;
        color: #EDEDED;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Hero Section */
    .hero-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #0066FF, #00C2FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        margin-top: -2rem;
    }
    .hero-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #888888;
        font-weight: 400;
        margin-bottom: 3rem;
    }

    /* Input Area */
    .stTextArea textarea {
        background-color: #121214 !important;
        color: #A0A0A0 !important;
        border: 1px solid #27272A !important;
        border-radius: 12px !important;
        font-family: 'Courier New', Courier, monospace !important;
        padding: 1rem !important;
        font-size: 0.9rem !important;
        box-shadow: inset 0px 2px 10px rgba(0,0,0,0.5);
    }
    .stTextArea textarea:focus {
        border-color: #0066FF !important;
        box-shadow: 0 0 0 2px rgba(0, 102, 255, 0.2) !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0066FF, #0047FF);
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 0 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0px 8px 25px rgba(0, 102, 255, 0.3) !important;
        width: 100%;
        margin-top: 1.5rem;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 12px 30px rgba(0, 102, 255, 0.5) !important;
        background: linear-gradient(90deg, #0077FF 0%, #0055FF 100%);
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: #121214;
        border: 1px solid #27272A;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: #888888 !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem;
    }

    /* Alert Boxes (Custom Banners) */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        padding: 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    div.stAlert[data-baseweb="notification"]:has(div:contains("🚨")) {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.15) 0%, rgba(153, 27, 27, 0.3) 100%) !important;
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
        color: #FCA5A5 !important;
        box-shadow: 0 0 20px rgba(220, 38, 38, 0.2) !important;
    }
    
    div.stAlert[data-baseweb="notification"]:has(div:contains("✅")) {
        background: linear-gradient(135deg, rgba(22, 163, 74, 0.15) 0%, rgba(21, 128, 61, 0.3) 100%) !important;
        border: 1px solid rgba(34, 197, 94, 0.4) !important;
        color: #86EFAC !important;
        box-shadow: 0 0 20px rgba(22, 163, 74, 0.2) !important;
    }

    /* Custom XAI Bar */
    .xai-container {
        background-color: #121214;
        border: 1px solid #27272A;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    .xai-title {
        color: #FFFFFF;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #27272A;
        padding-bottom: 0.5rem;
    }
    .xai-item {
        margin-bottom: 1rem;
    }
    .xai-label {
        display: flex;
        justify-content: space-between;
        color: #A0A0A0;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.3rem;
    }
    .xai-bar-bg {
        width: 100%;
        background-color: #27272A;
        border-radius: 99px;
        height: 10px;
        overflow: hidden;
    }
    .xai-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #0066FF, #00C2FF);
        border-radius: 99px;
    }
    
    /* BULLETPROOF SIDE-BY-SIDE LAYOUT (KILLS FLEXBOX STACKING) */
    [data-testid="stHorizontalBlock"], .stHorizontalBlock {
        display: block !important;
        background-color: #121214 !important;
        border: 1px solid #27272A !important;
        border-radius: 16px !important;
        padding: 30px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
        width: 100% !important;
        clear: both !important;
    }
    
    [data-testid="column"], .stColumn {
        display: inline-block !important;
        width: 48% !important;
        vertical-align: top !important;
        float: left !important;
    }
    
    [data-testid="column"]:nth-child(2), .stColumn:nth-child(2) {
        margin-left: 3% !important;
    }
    
    /* Clearfix for floats */
    [data-testid="stHorizontalBlock"]::after, .stHorizontalBlock::after {
        content: "";
        clear: both;
        display: table;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="hero-title">Ağ Anomali Tespiti</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Gerçek zamanlı trafik akışını analiz edin ve siber tehditleri tespit edin.</div>', unsafe_allow_html=True)

# Varsayılan JSON girdisi
sample_input = {
    "Destination Port": 80,
    "Flow Duration": 0.0,
    "Total Fwd Packets": 10,
    "Total Backward Packets": 5,
    "Total Length of Fwd Packets": 0.0,
    "Total Length of Bwd Packets": 0.0,
    "Fwd Packet Length Max": 0.0,
    "Fwd Packet Length Min": 0.0,
    "Fwd Packet Length Mean": 0.0,
    "Fwd Packet Length Std": 0.0,
    "Bwd Packet Length Max": 0.0,
    "Bwd Packet Length Min": 0.0,
    "Bwd Packet Length Mean": 0.0,
    "Bwd Packet Length Std": 0.0,
    "Flow Bytes/s": 0.0,
    "Flow Packets/s": 0.0,
    "Flow IAT Mean": 0.0,
    "Flow IAT Std": 0.0,
    "Flow IAT Max": 0.0,
    "Flow IAT Min": 0.0,
    "Fwd IAT Total": 0.0,
    "Fwd IAT Mean": 0.0,
    "Fwd IAT Std": 0.0,
    "Fwd IAT Max": 0.0,
    "Fwd IAT Min": 0.0,
    "Bwd IAT Total": 0.0,
    "Bwd IAT Mean": 0.0,
    "Bwd IAT Std": 0.0,
    "Bwd IAT Max": 0.0,
    "Bwd IAT Min": 0.0,
    "Fwd PSH Flags": 0.0,
    "Bwd PSH Flags": 0.0,
    "Fwd URG Flags": 0.0,
    "Bwd URG Flags": 0.0,
    "Fwd Header Length": 0.0,
    "Bwd Header Length": 0.0,
    "Fwd Packets/s": 0.0,
    "Bwd Packets/s": 0.0,
    "Min Packet Length": 0.0,
    "Max Packet Length": 0.0,
    "Packet Length Mean": 0.0,
    "Packet Length Std": 0.0,
    "Packet Length Variance": 0.0,
    "FIN Flag Count": 0.0,
    "SYN Flag Count": 0.0,
    "RST Flag Count": 0.0,
    "PSH Flag Count": 0.0,
    "ACK Flag Count": 0.0,
    "URG Flag Count": 0.0,
    "CWE Flag Count": 0.0,
    "ECE Flag Count": 0.0,
    "Down/Up Ratio": 0.0,
    "Average Packet Size": 0.0,
    "Avg Fwd Segment Size": 0.0,
    "Avg Bwd Segment Size": 0.0,
    "Fwd Header Length.1": 0.0,
    "Fwd Avg Bytes/Bulk": 0.0,
    "Fwd Avg Packets/Bulk": 0.0,
    "Fwd Avg Bulk Rate": 0.0,
    "Bwd Avg Bytes/Bulk": 0.0,
    "Bwd Avg Packets/Bulk": 0.0,
    "Bwd Avg Bulk Rate": 0.0,
    "Subflow Fwd Packets": 0.0,
    "Subflow Fwd Bytes": 0.0,
    "Subflow Bwd Packets": 0.0,
    "Subflow Bwd Bytes": 0.0,
    "Init_Win_bytes_forward": 0.0,
    "Init_Win_bytes_backward": 0.0,
    "act_data_pkt_fwd": 0.0,
    "min_seg_size_forward": 0.0,
    "Active Mean": 0.0,
    "Active Std": 0.0,
    "Active Max": 0.0,
    "Active Min": 0.0,
    "Idle Mean": 0.0,
    "Idle Std": 0.0,
    "Idle Max": 0.0,
    "Idle Min": 0.0
}

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = os.getenv("API_PORT", "8000")
api_url = f"http://{API_HOST}:{API_PORT}/predict"

# İki Sütunlu Yapı (Aynı frame)
col_input, col_results = st.columns(2)

# Sol Sütun - Kontrol Paneli
with col_input:
    st.markdown("<h3 style='margin-bottom:10px;'>Kontrol Paneli</h3>", unsafe_allow_html=True)
    st.caption("Ağ özelliklerini doğrudan JSON formatında düzenleyin (79 Feature):")
    st.markdown("<p style='font-size:0.8rem; color:#888888; margin-top:-10px;'>💡 Not: Kendi canlı ağ trafiğinizi bu JSON formatına dönüştürmek için <b>CICFlowMeter</b> aracını kullanabilirsiniz.</p>", unsafe_allow_html=True)
    json_input_str = st.text_area("JSON Input", json.dumps(sample_input, indent=2), height=450, label_visibility="collapsed")
    predict_clicked = st.button("Trafiği Analiz Et", use_container_width=True)

# Sağ Sütun - Analiz Sonuçları
with col_results:
    st.markdown("<h3 style='margin-bottom:10px;'>Analiz Sonuçları</h3>", unsafe_allow_html=True)

    if not predict_clicked:
        # Bekleme Ekranı
        st.info("Sistem hazır. Analiz başlatmak için soldaki paneli kullanın.")
    else:
        try:
            features = json.loads(json_input_str)
            with st.spinner("Model tahmin üretiyor..."):
                response = requests.post(api_url, json={"features": features})
            
            if response.status_code == 200:
                result = response.json()
                
                # Sınıfı Türkçe ve anlaşılır hale getirme
                durum_metni = "Güvenli" if result['class'] == "Normal" else "Riskli"
                
                # Metrik Kartları
                m1, m2 = st.columns(2)
                m1.metric("Ağ Trafiği Durumu", durum_metni)
                
                # Olasılığı Yüzdeye Çevir
                prob_pct = result['probability'] * 100
                m2.metric("Saldırı İhtimali", f"%{prob_pct:.2f}")
                
                # Büyük Alarm Kutusu
                if result['class'] == "Anomaly":
                    st.error("🚨 KRİTİK: AĞDA SİBER SALDIRI VEYA ANOMALİ TESPİT EDİLDİ 🚨")
                else:
                    st.success("✅ GÜVENLİ: NORMAL AĞ TRAFİĞİ")
                    
                # XAI Görselleştirmesi (HTML Progress Bar)
                if 'explanation' in result and 'top_features' in result['explanation']:
                    xai_data = result['explanation']['top_features']
                    
                    # İnsanların anlayacağı şekilde özellik çevirileri
                    feature_translations = {
                        "Fwd_Bwd_Ratio": "Gelen/Giden Paket Oranı",
                        "Total Backward Packets": "Toplam Gelen Paket Sayısı",
                        "Total Fwd Packets": "Toplam Giden Paket Sayısı",
                        "Destination Port": "Hedef Port (Bağlantı Noktası)",
                        "Flow Duration": "Bağlantı Süresi (Milisaniye)",
                        "Total Length of Fwd Packets": "Giden Verinin Toplam Boyutu",
                        "Total Length of Bwd Packets": "Gelen Verinin Toplam Boyutu",
                        "Flow Bytes/s": "Saniyedeki Veri Transfer Hızı (Bayt)",
                        "Flow Packets/s": "Saniyedeki Paket Transfer Hızı",
                        "Average Packet Size": "Ortalama Paket Boyutu",
                        "Down/Up Ratio": "İndirme/Yükleme Oranı"
                    }
                    
                    html_content = '<div class="xai-container"><div class="xai-title">Risk Analizi Detayları: Bu Karar Neden Verildi?</div>'
                    
                    # En yüksek değeri bul (bar genişliği için oranlama)
                    max_importance = max([feat['importance'] for feat in xai_data]) if xai_data else 1.0
                    if max_importance == 0: max_importance = 1.0
                    
                    for feat in xai_data:
                        raw_name = feat['feature']
                        # Sözlükte varsa Türkçe karşılığını al, yoksa alt çizgileri temizle
                        name = feature_translations.get(raw_name, raw_name.replace('_', ' ').title())
                        
                        val = feat['importance']
                        width = (val / max_importance) * 100
                        html_content += f'''
<div class="xai-item">
    <div class="xai-label"><span>{name}</span><span>Etki Skoru: {val:.4f}</span></div>
    <div class="xai-bar-bg">
        <div class="xai-bar-fill" style="width: {width}%;"></div>
    </div>
</div>
'''
                    html_content += '</div>'
                    st.markdown(html_content, unsafe_allow_html=True)
                    
            else:
                if response.status_code == 422:
                    st.error(f"Validation Error (Missing Features): {response.json().get('detail')}")
                else:
                    st.error(f"Error from API (HTTP {response.status_code}): {response.text}")
        except Exception as e:
            st.error(f"Error parsing JSON or calling API: {e}")
