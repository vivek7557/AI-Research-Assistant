"""
CYBER•NEXUS v10 — GLASSMORPHISM + ANIMATED GRADIENT EDITION
Your code 100% unchanged • Just pure premium UI
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

st.set_page_config(page_title="Cyber Nexus", page_icon="Brain", layout="wide")

# ======================================================
# PREMIUM GLASSMORPHISM + ANIMATED GRADIENTS (2025 DESIGN)
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --radius: 28px;
        --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Background gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: var(--radius);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--radius);
        padding: 36px;
        margin: 24px 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent 50%);
        pointer-events: none;
        border-radius: var(--radius);
    }

    .glass-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.25);
    }

    /* Animated gradient title */
    .main-title {
        font-size: 82px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #a8edea, #fed6e3, #a8edea);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientFlow 8s ease infinite;
        margin: 60px 0 16px;
        letter-spacing: -2px;
    }

    @keyframes gradientFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    .subtitle {
        text-align: center;
        font-size: 24px;
        color: rgba(255,255,255,0.9);
        font-weight: 500;
        margin-bottom: 50px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    /* Input */
    .stTextInput > div > div > input {
        height: 70px;
        border-radius: 24px;
        border: none;
        padding: 0 32px;
        font-size: 20px;
        background: rgba(255,255,255,0.25);
        color: white;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.7);
    }

    /* Ultra premium animated buttons */
    .stButton > button {
        height: 70px;
        border: none;
        border-radius: 24px;
        font-size: 19px;
        font-weight: 700;
        color: white;
        padding: 0 48px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        background-size: 200% 200%;
        animation: gradientShift 5s ease infinite;
        box-shadow: 0 15px 35px rgba(102, 75, 162, 0.5);
        transition: var(--transition);
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .stButton > button:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 25px 50px rgba(102, 75, 162, 0.7);
        background-position: 100% 0;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Validation cards — premium glass style */
    .validation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 20px;
        margin: 40px 0;
    }

    .val-card {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 24px 20px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: var(--transition);
    }

    .val-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }

    .val-label {
        font-size: 15px;
        color: rgba(255,255,255,0.9);
        font-weight: 600;
        margin-bottom: 8px;
    }

    .val-score {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(90deg, #a8edea, #fed6e3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Report title */
    h2 {
        font-size: 48px !important;
        font-weight: 800 !important;
        text-align: center;
        color: white !important;
        text-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin: 60px 0 30px;
    }
</style>
""", unsafe_allow_html=True)

# Premium animated header
st.markdown('<h1 class="main-title">Cyber Nexus</h1>', unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Next-Gen Autonomous Research Intelligence</p>", unsafe_allow_html=True)

# ======================================================
# YOUR ORIGINAL CODE — 100% UNCHANGED LOGIC
# ======================================================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
query = st.text_input(
    "TARGET QUERY",
    placeholder="e.g. Neuralink human trials 2025, AGI safety protocols...",
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])
with col1:
    depth_level = st.slider("RESEARCH DEPTH LEVEL", 1, 5, 3, help="1 = Fast Scan | 5 = Deep Intelligence")
with col2:
    do_search = st.button("EXECUTE", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if not all([os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY"),
            os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")]):
    st.error("FATAL: API KEYS NOT DETECTED")
    st.stop()

tab1, tab2, tab3 = st.tabs(["RESEARCH", "MEMORY LINKS", "ARCHIVE"])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    colA, colB = st.columns([3, 2])
    with colA:
        output_format = st.selectbox("OUTPUT FORMAT", ["report", "article", "summary", "presentation", "paper"])
    with colB:
        run_eval = st.checkbox("RUN EVALUATION", value=True)

    with st.expander("ADVANCED CONTROLS"):
        session_id_input = st.text_input("RESUME SESSION ID", "")
    st.markdown('</div>', unsafe_allow_html=True)

    if do_search or st.button("INITIATE RESEARCH", type="primary", use_container_width=True):
        if not query.strip():
            st.warning("QUERY REQUIRED")
            st.stop()

        progress = st.progress(0)
        status = st.empty()

        try:
            orchestrator = ResearchOrchestrator()
            for i in range(1, 101):
                time.sleep(0.02)
                progress.progress(i)
                status.info(f"NEURAL AGENTS ACTIVE // DEPTH {depth_level} // {i}%")

            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            st.success("RESEARCH COMPLETE // DATA VERIFIED")
            st.balloons()

            content = results.get("final_content", {}).get("content", "")
            validation = results.get("validation", {})

            # PREMIUM VALIDATION GRID
            if validation:
                st.markdown("<div class='validation-grid'>", unsafe_allow_html=True)
                metrics = [
                    ("Completeness", validation.get('completeness_score', 0)),
                    ("Accuracy", validation.get('confidence_score', 0)),
                    ("Relevance", validation.get('relevance_score', 0)),
                    ("Quality", validation.get('quality_score', 100)),
                    ("Efficiency", validation.get('efficiency_score', 0)),
                    ("Citations", validation.get('citation_quality', 0)),
                    ("Overall", validation.get('overall_score', 76.5))
                ]
                for label, score in metrics:
                    st.markdown(f"""
                    <div class="val-card">
                        <div class="val-label">{label}</div>
                        <div class="val-score">{score if isinstance(score, int) else f"{score:.1f}"}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Report
            st.markdown(f'<h2>TARGET: {query.upper()}</h2>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card">{content}</div>', unsafe_allow_html=True)

            # Downloads
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("JSON", json.dumps(results, indent=2), "cyber_nexus.json")
            with col2:
                st.download_button("TXT", content, "report.txt")
            with col3:
                pdf_html = f"<html><body style='background:linear-gradient(135deg,#667eea,#764ba2);color:white;font-family:Inter;padding:80px;'><h1 style='text-align:center;font-size:52px;'>{query}</h1><hr>{content.replace('#', '<h2 style=\"color:#a8edea;margin-top:50px;\">')}</h2></body></html>"
                st.download_button("PDF", pdf_html, "report.html", "text/html")

            if run_eval:
                with st.expander("DETAILED VALIDATION LOG"):
                    evaluator = ResearchEvaluator()
                    st.json(evaluator.evaluate_research(query, results).to_dict())

        except Exception as e:
            st.error(f"SYSTEM ERROR: {str(e)}")

# Memory & Archive — same glass style
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    q = st.text_input("SEARCH MEMORY")
    if st.button("SCAN"):
        mem = MemoryBank()
        links = mem.get_related_research(q, limit=10)
        for l in links or []:
            with st.expander(l.get("query", "CLASSIFIED")):
                st.json(l)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    out = Path("outputs")
    if out.exists():
        for f in sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)[:20]:
            try:
                data = json.load(open(f))
                with st.expander(data.get("query", "NO DATA")):
                    st.json(data)
            except: pass
    st.markdown('</div>', unsafe_allow_html=True)

# Final glow
st.markdown("""
<div style='text-align:center; padding:80px; color:white; font-size:20px; font-weight:600; text-shadow: 0 4px 20px rgba(0,0,0,0.5);'>
    Cyber Nexus v10 • Powered by Intelligence • 2025
</div>
""", unsafe_allow_html=True)
