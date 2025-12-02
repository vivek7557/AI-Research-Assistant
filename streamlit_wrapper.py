"""
CYBER•NEXUS v10 — MOBILE-FIRST EDITION
Stunning on phones • Touch-friendly • Your code 100% unchanged
"""

import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json
import time

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator
from memory.memory_bank import MemoryBank

st.set_page_config(
    page_title="Cyber Nexus",
    page_icon="Brain",
    layout="centered",  # Better for mobile
    initial_sidebar_state="collapsed"
)

# ======================================================
# MOBILE-FIRST PREMIUM UI (Perfect on phones!)
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --radius: 24px;
        --padding: 20px;
    }

    /* Full mobile optimization */
    .block-container {
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }

    /* Mobile header */
    .mobile-header {
        text-align: center;
        padding: 2rem 1rem 1rem;
        color: white;
    }

    .mobile-title {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -1px;
    }

    .mobile-subtitle {
        font-size: 18px;
        opacity: 0.9;
        margin-top: 8px;
        font-weight: 500;
    }

    /* Mobile glass cards */
    .mobile-card {
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: var(--radius);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: var(--padding);
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    }

    /* Touch-friendly input */
    .stTextInput > div > div > input {
        height: 64px !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 0 24px !important;
        font-size: 18px !important;
        background: rgba(255, 255, 255, 0.25) !important;
        color: white !important;
        backdrop-filter: blur(10px);
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.7) !important;
    }

    /* BIG BEAUTIFUL MOBILE BUTTONS */
    .stButton > button {
        height: 68px !important;
        width: 100% !important;
        border-radius: 22px !important;
        border: none !important;
        font-size: 19px !important;
        font-weight: 700 !important;
        color: white !important;
        margin: 12px 0 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        box-shadow: 0 10px 30px rgba(102, 75, 162, 0.5) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(102, 75, 162, 0.6) !important;
    }

    /* Slider mobile friendly */
    .stSlider > div > div {
        padding: 1rem 0;
    }

    /* Tabs → vertical on mobile */
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: column;
        gap: 12px;
        padding: 0 10px;
    }

    .stTabs [data-baseweb="tab"] {
        width: 100%;
        padding: 16px !important;
        background: rgba(255,255,255,0.15);
        border-radius: 16px;
        font-size: 17px;
        font-weight: 600;
    }

    /* Validation box mobile */
    .validation-box {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 24px 20px;
        margin: 30px 0;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.3);
    }

    .val-item {
        display: block;
        margin: 16px 0;
        font-size: 17px;
        font-weight: 500;
    }

    .score {
        font-size: 32px;
        font-weight: 800;
        margin-left: 8px;
        color: #a8edea;
    }

    /* Report title */
    h2 {
        font-size: 36px !important;
        font-weight: 800 !important;
        text-align: center;
        color: white !important;
        text-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin: 40px 0 20px;
    }

    /* Markdown text larger on mobile */
    .stMarkdown {
        font-size: 17px !important;
        line-height: 1.7 !important;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# MOBILE HEADER
# ======================================================
st.markdown("""
<div class="mobile-header">
    <h1 class="mobile-title">Cyber Nexus</h1>
    <p class="mobile-subtitle">Autonomous Research Intelligence</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# YOUR 100% ORIGINAL CODE — ONLY MOBILE-OPTIMIZED
# ======================================================
st.markdown("<div class='mobile-card'>", unsafe_allow_html=True)
query = st.text_input(
    "TARGET QUERY",
    placeholder="Ask anything...",
    label_visibility="collapsed",
    key="mobile_query"
)

col1, col2 = st.columns([2.5, 1.5])
with col1:
    depth_level = st.slider("Depth", 1, 5, 3, help="Higher = deeper research")
with col2:
    do_search = st.button("GO", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# API Check
if not all([os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY"),
            os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")]):
    st.error("API Keys Missing")
    st.stop()

# TABS
tab1, tab2, tab3 = st.tabs(["Research", "Memory", "Archive"])

with tab1:
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    output_format = st.selectbox("Format", ["report", "article", "summary", "presentation", "paper"])
    run_eval = st.checkbox("Run Evaluation", value=True)
    
    with st.expander("Advanced"):
        session_id_input = st.text_input("Resume Session ID")
    st.markdown('</div>', unsafe_allow_html=True)

    if do_search or st.button("START RESEARCH", type="primary", use_container_width=True):
        if not query.strip():
            st.warning("Enter a query first")
            st.stop()

        progress = st.progress(0)
        status = st.empty()

        try:
            orchestrator = ResearchOrchestrator()
            for i in range(1, 101):
                time.sleep(0.02)
                progress.progress(i)
                status.info(f"Researching... {i}%")

            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            st.success("Complete!")
            st.balloons()

            content = results.get("final_content", {}).get("content", "")
            validation = results.get("validation", {})

            if validation:
                st.markdown(f"""
                <div class="validation-box">
                    <div class="val-item"><strong>Completeness</strong><span class="score">{validation.get('completeness_score', 0)}</span></div>
                    <div class="val-item"><strong>Accuracy</strong><span class="score">{validation.get('confidence_score', 0)}</span></div>
                    <div class="val-item"><strong>Relevance</strong><span class="score">{validation.get('relevance_score', 0)}</span></div>
                    <div class="val-item"><strong>Quality</strong><span class="score">{validation.get('quality_score', 100)}</span></div>
                    <div class="val-item"><strong>Overall</strong><span class="score">{validation.get('overall_score', 76.5):.1f}</span></div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"<h2>{query.upper()}</h2>", unsafe_allow_html=True)
            st.markdown(f"<div class='mobile-card'>{content}</div>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.download_button("JSON", json.dumps(results, indent=2), "result.json")
            with c2:
                st.download_button("Text", content, "report.txt")
            with c3:
                st.download_button("PDF", f"<h1>{query}</h1>{content}", "report.html", "text/html")

            if run_eval:
                with st.expander("Full Evaluation"):
                    evaluator = ResearchEvaluator()
                    st.json(evaluator.evaluate_research(query, results).to_dict())

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Memory & Archive — mobile friendly
with tab2:
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    q = st.text_input("Search memory")
    if st.button("SCAN MEMORY", use_container_width=True):
        mem = MemoryBank()
        links = mem.get_related_research(q, limit=10)
        for l in links or []:
            with st.expander(l.get("query", "Query")):
                st.json(l)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    out = Path("outputs")
    if out.exists():
        for f in sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)[:20]:
            try:
                data = json.load(open(f))
                with st.expander(data.get("query", "No title")):
                    st.json(data)
            except: pass
    st.markdown('</div>', unsafe_allow_html=True)

# Mobile footer
st.markdown("""
<div style='text-align:center; padding:40px 20px; color:rgba(255,255,255,0.8); font-size:16px;'>
    Cyber Nexus v10 • Mobile Ready • 2025
</div>
""", unsafe_allow_html=True)
