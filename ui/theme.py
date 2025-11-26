import streamlit as st

def load_theme():
    st.markdown("""
    <style>

    /* --- GLOBAL PAGE CLEANUP --- */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px;
    }

    body, .stApp {
        background: #0d1117 !important;
    }

    /* --- PAGE TITLES --- */
    .page-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .section-title {
        margin-top: 1.5rem;
        font-size: 1.35rem;
        color: #cbd5e1;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    /* --- METRIC CARD --- */
    .metric-card {
        display: flex;
        gap: 12px;
        padding: 14px;
        background: #161b22;
        border: 1px solid #1f2937;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        align-items: center;
        transition: 0.25s;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #818cf8;
        box-shadow: 0 4px 14px rgba(129,140,248,0.35);
    }
    .metric-icon {
        font-size: 1.8rem;
    }
    .metric-title {
        font-size: 0.88rem;
        color: #94a3b8;
    }
    .metric-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e2e8f0;
    }

    /* --- RECENT LIST ITEM --- */
    .recent-item {
        background: #161b22;
        border: 1px solid #1f2937;
        padding: 10px 14px;
        border-radius: 10px;
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
        transition: 0.25s;
    }
    .recent-item:hover {
        border-color: #818cf8;
        background: #1e2637;
    }
    .recent-text {
        color: #cbd5e1;
        font-size: 0.9rem;
    }
    .recent-btn {
        background: #818cf8;
        color: white !important;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        text-decoration: none;
    }

    /* --- EVALUATION BARS --- */
    .eval-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 8px 0;
    }
    .eval-label {
        width: 150px;
        color: #cbd5e1;
        font-size: 0.9rem;
    }
    .eval-bar {
        flex-grow: 1;
        background: #1f2937;
        height: 6px;
        border-radius: 4px;
        overflow: hidden;
    }
    .eval-fill {
        background: #818cf8;
        height: 100%;
    }
    .eval-score {
        color: #e2e8f0;
        font-weight: 600;
        width: 40px;
        text-align: right;
    }

    </style>
    """, unsafe_allow_html=True)

