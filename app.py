import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
from datetime import datetime

from utils.prediction import predict_disease
from utils.recommendation_engine import get_recommendation
from utils.dosage_calculator import calculate_dosage
from utils.safety_alert import pesticide_safety
from utils.reminder import next_spray
from utils.history_manager import save_history
from utils.health_score import health_score
from utils.yield_estimator import yield_loss
from utils.fertilizer_engine import get_fertilizer
from utils.schedule_manager import save_schedule
from utils.translator import translate_text
from utils.weather_service import get_weather, spray_advice

st.set_page_config(
    page_title="Crop Disease Detection System",
    layout="centered",
    page_icon="",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    background-color: #e8f4fb !important;
    font-family: 'Outfit', sans-serif !important;
    color: #0f2d45 !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
section[data-testid="stSidebar"] {
    background: #c8e6f5 !important;
    border-right: 1px solid rgba(30, 100, 160, 0.12) !important;
}
.block-container {
    max-width: 720px !important;
    padding: 2rem 1.5rem 4rem !important;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* HEADER */
.app-header {
    text-align: center;
    padding: 1rem 0 2rem;
    animation: fadeInDown 0.8s ease-out forwards;
}
.app-title {
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin: 0 0 0.5rem;
    background: linear-gradient(135deg, #0077b6, #00b4d8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.app-sub {
    font-size: 0.8rem;
    color: #4a7fa5;
    letter-spacing: 4px;
    text-transform: uppercase;
    font-weight: 500;
}

/* SECTION LABEL */
.sec-label {
    font-size: 1.15rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #0f2d45;
    margin: 2.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 12px;
}
.sec-label::before { 
    content: ''; 
    width: 24px; 
    height: 3px;
    border-radius: 2px;
    background: linear-gradient(90deg, #0077b6, transparent); 
    transition: width 0.3s ease;
}
.sec-label:hover::before { width: 40px; }

/* CARDS */
.gcard {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(0, 119, 182, 0.12);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 16px -2px rgba(0, 100, 160, 0.08), 0 2px 6px -1px rgba(0, 100, 160, 0.04);
    animation: fadeInUp 0.6s ease-out forwards;
}
.gcard:hover {
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 20px 30px -8px rgba(0, 100, 160, 0.14), 0 8px 12px -4px rgba(0, 100, 160, 0.08);
    border-color: rgba(0, 119, 182, 0.25);
}
.gcard-green  { border-left: 4px solid #0096c7; }
.gcard-red    { border-left: 4px solid #e63946; }
.gcard-amber  { border-left: 4px solid #f4a261; }
.gcard-violet { border-left: 4px solid #4361ee; }
.gcard-cyan   { border-left: 4px solid #00b4d8; }
.gcard-blue   { border-left: 4px solid #0077b6; }

/* DETECTION RESULT */
.result-tag {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.tag-healthy {
    background: rgba(0, 150, 199, 0.12);
    color: #0077b6;
    border: 1px solid rgba(0, 119, 182, 0.3);
}
.tag-disease {
    background: rgba(230, 57, 70, 0.1);
    color: #e63946;
    border: 1px solid rgba(230, 57, 70, 0.3);
}
.result-name {
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0.5rem 0 0.2rem;
}
.result-meta  { font-size: 0.85rem; color: #4a7fa5; }
.result-score { font-size: 0.85rem; color: #6b9ab8; margin-top: 0.5rem; }

/* STAT ROW */
.stat-row {
    display: flex;
    gap: 16px;
    width: 100%;
    margin-bottom: 1rem;
}
.stat-box {
    flex: 1;
    min-width: 0;
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(0, 119, 182, 0.1);
    border-radius: 16px;
    padding: 1.2rem;
    transition: all 0.3s ease;
}
.stat-box:hover {
    transform: translateY(-2px);
    background: rgba(255, 255, 255, 0.85);
    border-color: rgba(0, 119, 182, 0.2);
}
.stat-label {
    font-size: 0.7rem;
    color: #4a7fa5;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 0 0 0.5rem;
    font-weight: 500;
}
.stat-value {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    margin: 0;
}

/* WEATHER ROW */
.weather-row {
    display: flex;
    gap: 12px;
    width: 100%;
    margin-bottom: 1rem;
}
.weather-box {
    flex: 1;
    min-width: 0;
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(0, 119, 182, 0.1);
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    transition: all 0.2s ease;
}
.weather-box:hover {
    background: rgba(255, 255, 255, 0.85);
}
.weather-label {
    font-size: 0.65rem;
    color: #4a7fa5;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 0 0 0.5rem;
    font-weight: 500;
}
.weather-value {
    font-size: 1.4rem;
    font-weight: 700;
    line-height: 1.1;
    margin: 0;
    word-break: break-word;
}

/* INFO ROWS */
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.7rem 0;
    border-bottom: 1px solid rgba(0, 119, 182, 0.08);
    font-size: 0.9rem;
    transition: background 0.2s ease;
}
.info-row:hover {
    background: rgba(0, 119, 182, 0.04);
    border-radius: 8px;
    padding-left: 8px;
    padding-right: 8px;
    margin-left: -8px;
    margin-right: -8px;
}
.info-row:last-child { border-bottom: none; padding-bottom: 0; }
.info-key { color: #4a7fa5; font-weight: 500; }
.info-val { font-weight: 600; }

/* SCHEDULE PILL */
.sched-pill {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.8rem;
}
.pill-safe   { background: rgba(0, 150, 199, 0.12); color: #0077b6; border: 1px solid rgba(0, 119, 182, 0.3); }
.pill-warn   { background: rgba(244, 162, 97, 0.15); color: #e07b39; border: 1px solid rgba(244, 162, 97, 0.3); }
.pill-danger { background: rgba(230, 57, 70, 0.1); color: #e63946; border: 1px solid rgba(230, 57, 70, 0.3); }

/* COLORS */
.col-green  { color: #0096c7; }
.col-red    { color: #e63946; }
.col-blue   { color: #0077b6; }
.col-amber  { color: #e07b39; }
.col-violet { color: #4361ee; }
.col-cyan   { color: #00b4d8; }
.col-muted  { color: #0f2d45; }

/* UPLOAD PLACEHOLDER */
.upload-zone {
    background: rgba(255, 255, 255, 0.5);
    border: 2px dashed rgba(0, 119, 182, 0.3);
    border-radius: 24px;
    padding: 4rem 2rem;
    text-align: center;
    transition: all 0.3s ease;
}
.upload-zone:hover {
    border-color: #0077b6;
    background: rgba(255, 255, 255, 0.7);
    box-shadow: 0 0 30px rgba(0, 119, 182, 0.1);
}
.upload-title { font-size: 1.1rem; font-weight: 600; color: #0f2d45; margin: 0 0 0.5rem; }
.upload-sub   { font-size: 0.8rem; color: #4a7fa5; letter-spacing: 1px; }

/* HOW IT WORKS */
.steps-list { display: flex; flex-direction: column; gap: 12px; margin-top: 1rem; }
.step-card {
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(0, 119, 182, 0.1);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    transition: all 0.3s ease;
}
.step-card:hover {
    transform: translateX(8px);
    background: rgba(255, 255, 255, 0.85);
    border-color: rgba(0, 119, 182, 0.3);
}
.step-num {
    width: 42px;
    height: 42px;
    min-width: 42px;
    background: rgba(0, 119, 182, 0.1);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95rem;
    font-weight: 700;
    color: #0077b6;
    transition: all 0.3s ease;
}
.step-card:hover .step-num { 
    background: #0077b6; 
    color: #ffffff; 
    box-shadow: 0 4px 12px rgba(0, 119, 182, 0.3);
}
.step-name { font-size: 0.95rem; font-weight: 600; color: #0f2d45; margin: 0; }
.step-desc { font-size: 0.8rem; color: #4a7fa5; margin: 0.2rem 0 0; }

/* STATUS DOT */
.status-dot {
    width: 8px;
    height: 8px;
    background: #0096c7;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    box-shadow: 0 0 10px rgba(0, 150, 199, 0.5);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 150, 199, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(0, 150, 199, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 150, 199, 0); }
}

/* STREAMLIT OVERRIDES */
[data-testid="stFileUploader"] > div:first-child {
    background: rgba(255, 255, 255, 0.5) !important;
    border: 2px dashed rgba(0, 119, 182, 0.4) !important;
    border-radius: 20px !important;
}
[data-testid="stFileUploader"] > div:first-child:hover {
    background: rgba(255, 255, 255, 0.75) !important;
    border-color: #0077b6 !important;
    box-shadow: 0 0 25px rgba(0, 119, 182, 0.15) !important;
}
[data-testid="stFileUploader"] label {
    color: #0f2d45 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}
[data-testid="stFileUploader"] button,
[data-testid="stFileUploaderDropzone"] button {
    background: rgba(0, 119, 182, 0.08) !important;
    color: #0077b6 !important;
    border: 1px solid rgba(0, 119, 182, 0.3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"] button:hover,
[data-testid="stFileUploaderDropzone"] button:hover {
    background: #0077b6 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px rgba(0, 119, 182, 0.3) !important;
    transform: translateY(-2px) !important;
}
div[data-testid="stNumberInput"] input {
    background: rgba(255, 255, 255, 0.7) !important;
    border: 1px solid rgba(0, 119, 182, 0.2) !important;
    color: #0f2d45 !important;
    border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #0077b6 !important;
    box-shadow: 0 0 0 2px rgba(0, 119, 182, 0.15) !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255, 255, 255, 0.7) !important;
    border: 1px solid rgba(0, 119, 182, 0.2) !important;
    color: #0f2d45 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stSelectbox"] > div > div:hover {
    border-color: #0077b6 !important;
    background: rgba(255, 255, 255, 0.9) !important;
}
.stButton > button {
    background: linear-gradient(135deg, rgba(0, 119, 182, 0.08), rgba(0, 180, 216, 0.08)) !important;
    color: #0f2d45 !important;
    border: 1px solid rgba(0, 119, 182, 0.2) !important;
    border-radius: 12px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0077b6, #00b4d8) !important;
    color: #ffffff !important;
    border-color: transparent !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 20px -5px rgba(0, 119, 182, 0.35) !important;
}
[data-testid="stImage"] img {
    border-radius: 20px !important;
    border: 1px solid rgba(0, 119, 182, 0.15) !important;
    display: block !important;
    margin: 0 auto !important;
    max-height: 400px !important;
    object-fit: contain !important;
    box-shadow: 0 10px 25px -5px rgba(0, 100, 160, 0.15) !important;
}
div[data-testid="stMarkdownContainer"] p { color: #4a7fa5; }
label,
.stNumberInput label,
.stSelectbox label {
    color: #4a7fa5 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    margin-bottom: 0.5rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
    <div style='padding:1.4rem 0.5rem 0.8rem; text-align:center;'>
        <div style='font-size:1.1rem; font-weight:700; color:#0f2d45; letter-spacing:-0.3px;'>Plant Disease Detector</div>
        <div style='font-size:0.62rem; color:#6b9ab8; letter-spacing:2.5px; text-transform:uppercase; margin-top:0.3rem;'>Plant Health System</div>
    </div>
    <div style='background:rgba(0,119,182,0.08); border-radius:10px; padding:0.75rem 1rem; margin:0.5rem 0 1rem; border:1px solid rgba(0,119,182,0.2);'>
        <div style='font-size:0.7rem; font-weight:600; color:#0077b6; margin-bottom:0.3rem;'>System Status</div>
        <div style='font-size:0.7rem; color:#0096c7; display:flex; align-items:center; gap:6px;'>
            <span class='status-dot'></span>
            AI Model Ready
        </div>
    </div>
    <hr style='border:none; border-top:1px solid rgba(0,119,182,0.12); margin:0 0 1rem;'>
    """,
        unsafe_allow_html=True,
    )

    language = st.selectbox("Language", ["English", "Hindi", "Marathi"])

    st.markdown(
        """
    <hr style='border:none; border-top:1px solid rgba(0,119,182,0.12); margin:1rem 0;'>
    <div style='font-size:0.62rem; color:#6b9ab8; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:0.8rem;'>How to Use</div>
    """,
        unsafe_allow_html=True,
    )

    for num, title, desc in [
        ("01", "Upload", "Clear leaf photo"),
        ("02", "Detect", "AI diagnosis"),
        ("03", "Treat", "Get treatment plan"),
        ("04", "Protect", "Set reminders"),
    ]:
        st.markdown(
            f"""
        <div style='display:flex; align-items:center; gap:10px; padding:0.55rem 0.7rem;
                    border-radius:9px; margin-bottom:0.3rem;'>
            <span style='font-size:0.68rem; font-weight:700; color:#0077b6; min-width:22px;'>{num}</span>
            <span style='font-size:0.82rem; color:#4a7fa5;'>
                <strong style='color:#0f2d45; display:block; font-size:0.85rem;'>{title}</strong>
                {desc}
            </span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <hr style='border:none; border-top:1px solid rgba(0,119,182,0.12); margin:1rem 0;'>
    <div style='background:rgba(0,119,182,0.07); border-radius:10px; padding:0.9rem 1rem; border:1px solid rgba(0,119,182,0.15);'>
        <div style='font-size:0.68rem; color:#0077b6; font-weight:600; margin-bottom:0.4rem; text-transform:uppercase; letter-spacing:1px;'>Pro Tip</div>
        <div style='font-size:0.72rem; color:#4a7fa5; line-height:1.65;'>
            Use well-lit photos for more accurate disease detection. Focus on affected leaf areas.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class='app-header'>
    <div class='app-title'>AI Crop Disease Detection System</div>
    <div class='app-sub'>Upload &middot; Detect &middot; Treat &middot; Protect</div>
</div>
""",
    unsafe_allow_html=True,
)

# ── FILE UPLOAD ────────────────────────────────────────────────────────────────
st.markdown(
    f"<div class='sec-label'>{translate_text('Scan Leaf', language)}</div>",
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader(
    translate_text("Upload a crop leaf image", language),
    type=["jpg", "png", "jpeg"],
    label_visibility="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    max_w = 400
    if image.width > max_w:
        image = image.resize(
            (max_w, int(image.height * max_w / image.width)), Image.LANCZOS
        )
    st.image(image, use_container_width=False, width=max_w)

    img = np.array(image)
    disease, Detection_score = predict_disease(img)

    if "___" in disease:
        plant, disease_name = disease.split("___")
    else:
        plant, disease_name = "Unknown", disease

    disease_name = disease_name.replace("_", " ").title()
    is_healthy = "healthy" in disease.lower()

    pesticide, dosage, interval = get_recommendation(disease)
    save_history(plant, disease_name, Detection_score, pesticide)

    if Detection_score < 0.75:
        st.warning(translate_text("Low confidence — try a clearer image.", language))

    # Detection Result
    st.markdown(
        f"<div class='sec-label'>{translate_text('Detection Result', language)}</div>",
        unsafe_allow_html=True,
    )
    tag_cls = "tag-healthy" if is_healthy else "tag-disease"
    tag_txt = "Healthy Plant" if is_healthy else "Disease Detected"
    name_col = "#0077b6" if is_healthy else "#e63946"
    card_acc = "gcard-green" if is_healthy else "gcard-red"

    st.markdown(
        f"""
    <div class='gcard {card_acc}'>
        <span class='result-tag {tag_cls}'>{tag_txt}</span>
        <div class='result-name' style='color:{name_col};'>{disease_name}</div>
        <div class='result-meta'>Plant &nbsp;&middot;&nbsp; {plant}</div>
        <div class='result-score'>Detection_score &nbsp;<strong style='color:#1a4a6b;'>{Detection_score * 100:.1f}%</strong></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Crop Health
    st.markdown(
        f"<div class='sec-label'>{translate_text('Crop Health', language)}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
    <div class='stat-row'>
        <div class='stat-box'>
            <div class='stat-label'>Health Score</div>
            <div class='stat-value col-green'>{health_score(disease)}%</div>
        </div>
        <div class='stat-box'>
            <div class='stat-label'>Yield Loss</div>
            <div class='stat-value col-red'>{yield_loss(disease)}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Pesticide Recommendation
    st.markdown(
        f"<div class='sec-label'>{translate_text('Pesticide Recommendation', language)}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
    <div class='gcard gcard-green'>
        <div class='info-row'>
            <span class='info-key'>Recommended</span>
            <span class='info-val col-green'>{pesticide}</span>
        </div>
        <div class='info-row'>
            <span class='info-key'>Dosage per Litre</span>
            <span class='info-val col-muted'>{dosage}</span>
        </div>
        <div class='info-row'>
            <span class='info-key'>Spray Interval</span>
            <span class='info-val col-amber'>{interval}</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Dosage Calculator
    st.markdown(
        f"<div class='sec-label'>{translate_text('Dosage Calculator', language)}</div>",
        unsafe_allow_html=True,
    )
    tank = st.number_input(
        translate_text("Tank Size (Litres)", language),
        min_value=1,
        max_value=500,
        value=10,
        key="tank_input",
    )
    per_litre, total, unit = calculate_dosage(dosage, tank)
    st.markdown(
        f"""
    <div class='stat-row'>
        <div class='stat-box'>
            <div class='stat-label'>Per Litre</div>
            <div class='stat-value col-blue' style='font-size:1.5rem; margin-top:4px;'>{per_litre}</div>
        </div>
        <div class='stat-box'>
            <div class='stat-label'>For {tank} L</div>
            <div class='stat-value col-green' style='font-size:1.5rem; margin-top:4px;'>{total}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Fertilizer Recommendation
    fert, usage, freq = get_fertilizer(disease)
    st.markdown(
        f"<div class='sec-label'>{translate_text('Fertilizer Recommendation', language)}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
    <div class='gcard gcard-violet'>
        <div class='info-row'>
            <span class='info-key'>Fertilizer</span>
            <span class='info-val col-violet'>{fert}</span>
        </div>
        <div class='info-row'>
            <span class='info-key'>Usage</span>
            <span class='info-val col-cyan'>{usage}</span>
        </div>
        <div class='info-row'>
            <span class='info-key'>Frequency</span>
            <span class='info-val col-amber'>{freq}</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Safety Instructions
    st.markdown(
        f"<div class='sec-label'>{translate_text('Safety Instructions', language)}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
    <div class='gcard gcard-amber'>
        <div style='font-size:0.86rem; color:#4a7fa5; line-height:1.75;'>
            {pesticide_safety(pesticide)}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Weather-Based Spray Recommendation
    st.markdown(
        "<div class='sec-label'>Weather-Based Spray Advice</div>",
        unsafe_allow_html=True,
    )
    city = st.selectbox(
        "Select your city",
        ["Pune", "Mumbai", "Nagpur", "Delhi", "Bangalore", "Hyderabad", "Ahilyanagar"],
    )

    weather = get_weather(city) or {
        "temperature": 28,
        "humidity": 65,
        "condition": "Clear",
    }

    st.markdown(
        f"""
    <div class='weather-row'>
        <div class='weather-box'>
            <div class='weather-label'>Temperature</div>
            <div class='weather-value col-amber'>{weather["temperature"]}°C</div>
        </div>
        <div class='weather-box'>
            <div class='weather-label'>Humidity</div>
            <div class='weather-value col-blue'>{weather["humidity"]}%</div>
        </div>
        <div class='weather-box'>
            <div class='weather-label'>Condition</div>
            <div class='weather-value col-violet' style='font-size:1.05rem;'>{weather["condition"]}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    advice = spray_advice(weather)
    advice_acc = (
        "gcard-red"
        if "Avoid spraying" in advice
        else "gcard-amber"
        if "High humidity" in advice or "Too hot" in advice
        else "gcard-green"
    )
    st.markdown(
        f"""
    <div class='gcard {advice_acc}'>
        <div style='font-size:0.88rem; color:#0f2d45; line-height:1.6;'>
            <span style='font-weight:700; color:#1a4a6b;'>Spray Advice: </span>{advice}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Spray Schedule
    st.markdown(
        f"<div class='sec-label'>{translate_text('Next Spray Schedule', language)}</div>",
        unsafe_allow_html=True,
    )
    next_date = next_spray(interval)

    def days_remaining(nd):
        return (datetime.strptime(nd, "%d-%m-%Y") - datetime.today()).days

    days_left = days_remaining(next_date)
    if days_left <= 2:
        pill_cls, pill_txt = "pill-danger", "Spray due — act now"
    elif days_left <= 5:
        pill_cls, pill_txt = "pill-warn", "Spray coming up"
    else:
        pill_cls, pill_txt = "pill-safe", "Schedule on track"

    st.markdown(
        f"""
    <div class='gcard gcard-cyan'>
        <div class='info-row'>
            <span class='info-key'>Next Spray Date</span>
            <span class='info-val col-muted'>{next_date}</span>
        </div>
        <div class='info-row'>
            <span class='info-key'>Days Remaining</span>
            <span class='info-val col-cyan'>{days_left} days</span>
        </div>
        <div style='margin-top:0.4rem;'>
            <span class='sched-pill {pill_cls}'>{pill_txt}</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button(translate_text("Set Spray Reminder", language)):
        save_schedule(plant, disease_name, next_date)
        st.success(translate_text("Reminder saved successfully!", language))

    # History
    st.markdown(
        f"<div class='sec-label'>{translate_text('History', language)}</div>",
        unsafe_allow_html=True,
    )
    try:
        df = pd.read_csv("database/history.csv")
        st.dataframe(df.tail(5), use_container_width=True, hide_index=True)
    except Exception:
        st.info(translate_text("No history available yet.", language))

# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown(
        """
    <div class='upload-zone'>
        <div class='upload-title'>Drop a leaf image here to begin</div>
        <div class='upload-sub'>JPG &nbsp;&middot;&nbsp; PNG &nbsp;&middot;&nbsp; JPEG</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='sec-label'>How It Works</div>", unsafe_allow_html=True)
    st.markdown(
        """
    <div class='steps-list'>
        <div class='step-card'>
            <div class='step-num'>01</div>
            <div>
                <div class='step-name'>Upload</div>
                <div class='step-desc'>Upload a clear photo of the affected leaf</div>
            </div>
        </div>
        <div class='step-card'>
            <div class='step-num'>02</div>
            <div>
                <div class='step-name'>AI Detection</div>
                <div class='step-desc'>Our AI analyzes the image for diseases</div>
            </div>
        </div>
        <div class='step-card'>
            <div class='step-num'>03</div>
            <div>
                <div class='step-name'>Treatment Plan</div>
                <div class='step-desc'>Get recommended pesticides and dosages</div>
            </div>
        </div>
        <div class='step-card'>
            <div class='step-num'>04</div>
            <div>
                <div class='step-name'>Protect</div>
                <div class='step-desc'>Set reminders and monitor crop health</div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )