import streamlit as st

def load_theme():
    st.markdown("""
    <style>

    /* =============== GLOBAL =============== */
    .stApp {
        animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0px); }
    }

    body, .stApp {
        background: #0d1117 !important;
    }

    .block-container {
        padding-top: 1.2rem !important;
        max-width: 1100px;
        animation: slideUp 0.5s ease-out;
    }

    @keyframes slideUp {
        from { transform: translateY(15px); opacity: 0; }
        to   { transform: translateY(0px); opacity: 1; }
    }

    /* =============== TITLES =============== */
    .page-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glowIn 1s ease-out;
    }

    @keyframes glowIn {
        0%   { letter-spacing: -2px; opacity: 0; }
        100% { letter-spacing: 0px; opacity: 1; }
    }

    .section-title {
        margin-top: 1.5rem;
        font-size: 1.35rem;
        color: #cbd5e1;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    /* =============== METRIC CARDS =============== */
    .metric-card {
        display: flex;
        gap: 12px;
        padding: 14px;
        background: #161b22;
        border: 1px solid #1f2937;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        align-items: center;
        transition: 0.25s ease-in-out;
        animation: cardPop 0.4s ease-out;
    }

    @keyframes cardPop {
        0%   { transform: scale(0.9); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    .metric-card:hover {
        transform: translateY(-4px) scale(1.02);
        border-color: #818cf8;
        box-shadow: 0 6px 20px rgba(129,140,248,0.35);
    }

    /* =============== RECENT ITEM LIST =============== */
    .recent-item {
        background: #161b22;
        border: 1px solid #1f2937;
        padding: 10px 14px;
        border-radius: 10px;
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;

        transition: transform 0.2s ease, background 0.3s ease;
        animation: fadeSlide 0.5s ease;
    }

    @keyframes fadeSlide {
        from { opacity: 0; transform: translateX(-10px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    .recent-item:hover {
        transform: translateX(6px);
        background: #1e2637;
        border-color: #818cf8;
    }

    .recent-btn {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white !important;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        text-decoration: none;
        transition: 0.25s ease;
    }

    .recent-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 3px 10px rgba(129,140,248,0.35);
    }

    /* =============== EVALUATION BARS =============== */
    .eval-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 8px 0;
        animation: barIn 0.6s ease;
    }

    @keyframes barIn {
        from { opacity: 0; transform: translateX(-10px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    .eval-bar {
        flex-grow: 1;
        background: #1f2937;
        height: 8px;
        border-radius: 6px;
        overflow: hidden;
        position: relative;
    }

    .eval-fill {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        height: 100%;
        animation: barFill 1.5s ease-out;
    }

    @keyframes barFill {
        from { width: 0%; }
        to   { width: inherit; }
    }

    .eval-score {
        color: #e2e8f0;
        font-weight: 600;
        width: 40px;
        text-align: right;
    }

    /* SIDEBAR HOVER EFFECT */
    .css-1d391kg:hover, .css-1y4p8pa:hover {
        background-color: rgba(129,140,248,0.15) !important;
        transition: 0.3s;
    }

    </style>
    """, unsafe_allow_html=True)
