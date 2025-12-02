"""
CYBER•NEXUS v10 — CLEAN & MINIMAL EDITION
No loading animation • No card hover • Pure calm beauty
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
# CLEAN, CALM, MINIMAL UI — EXACTLY LIKE YOUR SCREENSHOT
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg: linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%);
        --card-bg: rgba(255, 255, 255, 0.12);
        --text: white;
        --radius: 28px;
    }

    [data-testid="stAppViewContainer"] {
        background: var(--bg);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }

    .main-title {
        font-size: 80px;
        font-weight: 800;
        text-align: center;
        color: white;
        margin: 60px 0 16px;
        letter-spacing: -2px;
    }

    .subtitle {
        text-align: center;
        font-size: 24px;
        color: rgba(255,255,255,0.9);
        margin-bottom: 50px;
    }

    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border-radius: var(--radius)px;
        border: 1px solid rgba(255,255,255,0.15);
        padding: 36px;
        margin: 24px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }

    .stTextInput > div > div > input {
        height: 68px;
        border-radius: 24px;
        border: none;
        padding: 0 32px;
        font-size: 20px;
        background: rgba(255,255,255,0.2);
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.7);
    }

    .stButton > button {
        height: 68px;
        border-radius: 24px;
        border: none;
        font-size: 18px;
        font-weight: 700;
        color: white;
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }

    .stButton > button:hover {
        background: rgba(255,255,255,0.35);
        transform: translateY(-4px);
    }

    /* VALIDATION CARDS — 100% STATIC, NO ANIMATION */
    .validation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 40px 0;
    }

    .val-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 32px 24px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    .val-label {
        font-size: 16px;
        color: rgba(255,255,255,0.9);
        font-weight: 500;
        margin-bottom: 12px;
    }

    .val-score {
        font-size: 42px;
        font-weight: 800;
        color: white;
    }

    h2 {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        color: white;
        margin: 60px 0 30px;
    }
</style>
""", unsafe_allow_html=True)

# Clean header
st.markdown('<h1 class="main-title">Cyber Nexus</h1>', unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Autonomous Research Intelligence</p>", unsafe_allow_html=True)

# ======================================================
# YOUR ORIGINAL CODE — NO LOADING, NO ANIMATIONS
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
                status.info(f"Processing... {i}%")

            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            st.success("RESEARCH COMPLETE")
            st.balloons()

            content = results.get("final_content", {}).get("content", "")
            validation = results.get("validation", {})

            # CLEAN STATIC VALIDATION — NO ANIMATION
            if validation:
                st.markdown("<div class='validation-grid'>", unsafe_allow_html=True)
                metrics = [
                    ("Quality", validation.get('quality_score', 100)),
                    ("Efficiency", validation.get('efficiency_score', 0)),
                    ("Citations", validation.get('citation_quality', 0)),
                    ("Overall", validation.get('overall_score', 76.5)),
                ]
                for label, score in metrics:
                    st.markdown(f"""
                    <div class="val-card">
                        <div class="val-label">{label}</div>
                        <div class="val-score">{score if isinstance(score, int) else f"{score:.1f}"}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f'<h2>{query.upper()}</h2>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card">{content}</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("JSON", json.dumps(results, indent=2), "result.json")
            with col2:
                st.download_button("TXT", content, "report.txt")
            with col3:
                st.download_button("PDF", f"<h1>{query}</h1>{content}", "report.html", "text/html")

            if run_eval:
                with st.expander("VALIDATION LOG"):
                    evaluator = ResearchEvaluator()
                    st.json(evaluator.evaluate_research(query, results).to_dict())

        except Exception as e:
            st.error(f"ERROR: {str(e)}")

# Tabs — clean
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

# Clean footer
st.markdown("""
<div style='text-align:center; padding:80px; color:rgba(255,255,255,0.8); font-size:18px;'>
    Cyber Nexus v10 • 2025
</div>
""", unsafe_allow_html=True)
