import streamlit as st
import pandas as pd
import numpy as np
from utils.translator import translate_text

st.set_page_config(
    page_title="Analytics - Crop Disease Detector", page_icon="📊", layout="wide"
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"] {
        background: linear-gradient(135deg, #e0f2fe, #f0f9ff) !important;
        font-family: 'Outfit', sans-serif !important;
        color: #0f172a !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] {
        background: #dbeafe !important;
        border-right: 1px solid rgba(59, 130, 246, 0.15) !important;
    }

    .main-header {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #2563eb, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .section-title {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #1e3a8a !important;
        padding: 0.6rem 1rem;
        border-left: 4px solid #3b82f6;
        background: linear-gradient(90deg, rgba(59,130,246,0.12) 0%, transparent 100%);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-radius: 6px;
        letter-spacing: 0.5px;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: 18px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 6px 15px rgba(59, 130, 246, 0.08);
    }

    .metric-card:hover {
        transform: translateY(-4px);
        background: rgba(255,255,255,0.95);
        box-shadow: 0 12px 20px rgba(59, 130, 246, 0.15);
    }

    .info-card {
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 4px solid #3b82f6;
        border: 1px solid rgba(59,130,246,0.1);
        box-shadow: 0 4px 10px rgba(59,130,246,0.08);
    }

    .success-card {
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 4px solid #0ea5e9;
        border: 1px solid rgba(14,165,233,0.1);
        box-shadow: 0 4px 10px rgba(14,165,233,0.08);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #0ea5e9) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(59,130,246,0.25);
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59,130,246,0.35);
    }

    label, .stSelectbox label {
        color: #1e3a8a !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.8) !important;
        border: 1px solid rgba(59,130,246,0.15) !important;
        color: #0f172a !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stSelectbox"] > div > div:hover {
        border-color: #3b82f6 !important;
        background: white !important;
    }

    .stDataFrame {
        background: rgba(255,255,255,0.7) !important;
        border-radius: 12px !important;
    }

</style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
    <div style='text-align: center; padding: 1.5rem 1rem;'>
        <div style='font-size:1.4rem; font-weight:700; color:#2563eb;'>
            Crop Disease Detector
        </div>
        <div style='color: #64748b; font-size:0.8rem; letter-spacing:2px;
                    text-transform:uppercase; margin-top:0.3rem;'>
            Analytics Panel
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    language = st.selectbox("Language", ["English", "Hindi", "Marathi"])

    st.markdown(
        "<hr style='border-top: 1px solid rgba(59,130,246,0.15);'>",
        unsafe_allow_html=True,
    )

    if st.button("Go to Home"):
        st.switch_page("app.py")

st.markdown(
    f"<h1 class='main-header'>Analytics Dashboard</h1>",
    unsafe_allow_html=True,
)

try:
    df = pd.read_csv("database/history.csv")

    total_records = len(df)

    healthy_count = (
        df[df["Disease"].str.lower().str.contains("healthy", na=False)].shape[0]
        if "Disease" in df.columns
        else 0
    )

    diseased_count = total_records - healthy_count

    st.markdown(
        f"<p class='section-title'>Overview</p>",
        unsafe_allow_html=True,
    )

    ov1, ov2, ov3, ov4 = st.columns(4)

    with ov1:
        st.markdown(
            f"""
        <div class='metric-card'>
            <p style='color:#64748b;font-size:0.75rem;
                      text-transform:uppercase;letter-spacing:1px;'>
                Total Scans
            </p>
            <p style='font-size:2.2rem;font-weight:bold;
                      color:#2563eb;'>
                {total_records}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with ov2:
        st.markdown(
            f"""
        <div class='metric-card'>
            <p style='color:#64748b;font-size:0.75rem;
                      text-transform:uppercase;letter-spacing:1px;'>
                Healthy Plants
            </p>
            <p style='font-size:2.2rem;font-weight:bold;
                      color:#10b981;'>
                {healthy_count}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with ov3:
        st.markdown(
            f"""
        <div class='metric-card'>
            <p style='color:#64748b;font-size:0.75rem;
                      text-transform:uppercase;letter-spacing:1px;'>
                Diseased
            </p>
            <p style='font-size:2.2rem;font-weight:bold;
                      color:#ef4444;'>
                {diseased_count}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with ov4:
        health_rate = (
            (healthy_count / total_records * 100)
            if total_records > 0
            else 0
        )

        st.markdown(
            f"""
        <div class='metric-card'>
            <p style='color:#64748b;font-size:0.75rem;
                      text-transform:uppercase;letter-spacing:1px;'>
                Health Rate
            </p>
            <p style='font-size:2.2rem;font-weight:bold;
                      color:#0ea5e9;'>
                {health_rate:.1f}%
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "<hr style='border-top: 1px solid rgba(59,130,246,0.1); margin: 2rem 0;'>",
        unsafe_allow_html=True,
    )

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown(
            "<p class='section-title'>Disease Distribution</p>",
            unsafe_allow_html=True,
        )

        if "Disease" in df.columns:
            disease_counts = df["Disease"].value_counts()
            st.bar_chart(disease_counts)

    with row1_col2:
        st.markdown(
            "<p class='section-title'>Plant Distribution</p>",
            unsafe_allow_html=True,
        )

        if "Plant" in df.columns:
            plant_counts = df["Plant"].value_counts()
            st.bar_chart(plant_counts)

    st.markdown(
        "<hr style='border-top: 1px solid rgba(59,130,246,0.1); margin: 2rem 0;'>",
        unsafe_allow_html=True,
    )

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown(
            "<p class='section-title'>Pesticide Usage</p>",
            unsafe_allow_html=True,
        )

        if "Pesticide" in df.columns:
            pesticide_counts = df["Pesticide"].value_counts().head(10)
            st.bar_chart(pesticide_counts)

    with row2_col2:
        st.markdown(
            "<p class='section-title'>Confidence Levels</p>",
            unsafe_allow_html=True,
        )

        if "Confidence" in df.columns:
            conf_bins = pd.cut(
                pd.to_numeric(df["Confidence"], errors="coerce").fillna(0),
                bins=[0, 0.5, 0.75, 0.9, 1.0],
                labels=[
                    "Low (<50%)",
                    "Medium (50-75%)",
                    "High (75-90%)",
                    "Very High (>90%)",
                ],
            )

            conf_counts = conf_bins.value_counts()
            st.bar_chart(conf_counts)

    st.markdown(
        "<hr style='border-top: 1px solid rgba(59,130,246,0.1); margin: 2rem 0;'>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='section-title'>Scan History</p>",
        unsafe_allow_html=True,
    )

    st.dataframe(
        df.tail(20),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "<hr style='border-top: 1px solid rgba(59,130,246,0.1); margin: 2rem 0;'>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='section-title'>Statistics Summary</p>",
        unsafe_allow_html=True,
    )

    if "Confidence" in df.columns:

        numeric_conf = (
            pd.to_numeric(df["Confidence"], errors="coerce")
            .dropna()
        )

        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

        with stat_col1:
            st.markdown(
                f"""
            <div class='metric-card'>
                <p style='color:#64748b;font-size:0.75rem;
                          text-transform:uppercase;'>
                    Avg Confidence
                </p>
                <p style='font-size:1.8rem;font-weight:bold;
                          color:#2563eb;'>
                    {(numeric_conf.mean() * 100) if not numeric_conf.empty else 0:.1f}%
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with stat_col2:
            st.markdown(
                f"""
            <div class='metric-card'>
                <p style='color:#64748b;font-size:0.75rem;
                          text-transform:uppercase;'>
                    Min Confidence
                </p>
                <p style='font-size:1.8rem;font-weight:bold;
                          color:#ef4444;'>
                    {(numeric_conf.min() * 100) if not numeric_conf.empty else 0:.1f}%
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with stat_col3:
            st.markdown(
                f"""
            <div class='metric-card'>
                <p style='color:#64748b;font-size:0.75rem;
                          text-transform:uppercase;'>
                    Max Confidence
                </p>
                <p style='font-size:1.8rem;font-weight:bold;
                          color:#10b981;'>
                    {(numeric_conf.max() * 100) if not numeric_conf.empty else 0:.1f}%
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with stat_col4:
            st.markdown(
                f"""
            <div class='metric-card'>
                <p style='color:#64748b;font-size:0.75rem;
                          text-transform:uppercase;'>
                    Std Deviation
                </p>
                <p style='font-size:1.8rem;font-weight:bold;
                          color:#f59e0b;'>
                    {(numeric_conf.std() * 100) if (not numeric_conf.empty and len(numeric_conf) > 1) else 0:.1f}%
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

except Exception as e:

    st.markdown(
        """
    <div class='info-card'>
        <h3 style='color:#2563eb;'>No analytics data yet</h3>
        <p style='color:#64748b;'>
            Upload crop leaf images on the main page to start analytics tracking.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<hr style='border-top: 1px solid rgba(59,130,246,0.1); margin: 2rem 0;'>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class='success-card'>
        <h3 style='color:#0f172a;'>What's Tracked</h3>
        <ul style='color:#475569;'>
            <li>Total number of plant scans</li>
            <li>Disease distribution</li>
            <li>Plant type analytics</li>
            <li>Pesticide usage statistics</li>
            <li>AI confidence levels</li>
            <li>Health rate tracking</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )