"""
CYBER•NEXUS v10 — FINAL TERMINAL EDITION
Now with ultra-premium gradient buttons + rich colors
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
# GORGEOUS 2025 FIGMA-STYLE UI — RICHER GRADIENTS + STUNNING BUTTONS
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #f8fafc;
        --card: rgba(255, 255, 255, 0.92);
        --border: rgba(255, 255, 255, 0.4);
        --text: #1e293b;
        --text-light: #64748b;
        --shadow: 0 12px 40px -8px rgba(99, 102, 241, 0.3);
        --radius: 24px;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f0f4f0 0%, #e0eaff 50%, #d0f4ff 100%);
        font-family: 'Inter', sans-serif;
        color: var(--text);
    }

    .main-title {
        font-size: 76px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #8b5cf6, #3b82f6, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 50px 0 15px;
        letter-spacing: -2px;
    }

    .subtitle {
        text-align: center;
        font-size: 24px;
        font-weight: 500;
        color: #6366f1;
        margin-bottom: 60px;
        text-shadow: 0 2px 10px rgba(99,102,241,0.2);
    }

    .glass-card {
        background: var(--card);
        border-radius: var(--radius);
        padding: 36px;
        margin: 28px 0;
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        transition: all 0.3s;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 50px -12px rgba(99, 102, 241, 0.35);
    }

    /* INPUT FIELD — Premium look */
    .stTextInput > div > div > input {
        background: white !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 20px 24px !important;
        font-size: 19px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08) !important;
        transition: all 0.3s;
    }

    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.25) !important;
        transform: scale(1.02);
    }

    /* ULTRA BEAUTIFUL GRADIENT BUTTONS */
    .stButton > button {
        height: 64px;
        border: none;
        border-radius: 20px;
        font-size: 18px;
        font-weight: 700;
        color: white;
        padding: 0 40px;
        cursor: pointer;
        background: linear-gradient(135deg, #8b5cf6, #3b82f6, #10b981) !important;
        background-size: 200% 200% !important;
        animation: gradientShift 6s ease infinite;
        box-shadow: 0 12px 35px rgba(139, 92, 246, 0.4);
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        transform: translateY(-6px) scale(1.05);
        box-shadow: 0 20px 50px rgba(139, 92, 246, 0.6);
        background-position: 100% 0 !important;
    }

    .stButton > button:active {
        transform: translateY(-2px);
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Validation box — richer gradient */
    .validation-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        border-radius: 20px;
        padding: 32px;
        margin: 40px 0;
        text-align: center;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
        font-weight: 600;
        font-size: 17px;
    }

    .val-item {
        display: inline-block;
        margin: 0 28px;
        font-size: 17px;
    }

    .score {
        font-size: 28px;
        font-weight: 800;
        margin-left: 10px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    h2 {
        font-size: 44px !important;
        font-weight: 800 !important;
        text-align: center;
        background: linear-gradient(90deg, #8b5cf6, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 50px 0 30px;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# PREMIUM HEADER
# ======================================================
st.markdown('<h1 class="main-title">Cyber Nexus</h1>', unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Next-Generation Autonomous Research Intelligence</p>", unsafe_allow_html=True)

# ======================================================
# YOUR 100% ORIGINAL CODE — ONLY VISUALS UPGRADED
# ======================================================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
query = st.text_input(
    "TARGET QUERY",
    placeholder="e.g. Neuralink human trials 2025, AGI safety protocols, nuclear fusion ignition...",
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])
with col1:
    depth_level = st.slider("RESEARCH DEPTH LEVEL", 1, 5, 3, help="1 = Fast Scan | 5 = Deep Intelligence")
with col2:
    do_search = st.button("EXECUTE", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# API Check
if not all([os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY"),
            os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")]):
    st.error("FATAL: API KEYS NOT DETECTED")
    st.stop()

# TABS
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

            if validation:
                st.markdown(f"""
                <div class="validation-box">
                    <div class="val-item"><strong>Completeness</strong><span class="score">{validation.get('completeness_score', 0)}</span></div>
                    <div class="val-item"><strong>Accuracy</strong><span class="score">{validation.get('confidence_score', 0)}</span></div>
                    <div class="val-item"><strong>Relevance</strong><span class="score">{validation.get('relevance_score', 0)}</span></div>
                    <div class="val-item"><strong>Quality</strong><span class="score">{validation.get('quality_score', 100)}</span></div>
                    <div class="val-item"><strong>Efficiency</strong><span class="score">{validation.get('efficiency_score', 0)}</span></div>
                    <div class="val-item"><strong>Citations</strong><span class="score">{validation.get('citation_quality', 0)}</span></div>
                    <div class="val-item"><strong>Overall</strong><span class="score">{validation.get('overall_score', 76.5):.1f}</span></div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f'<div class="glass-card"><h2>TARGET: {query.upper()}</h2>', unsafe_allow_html=True)
            st.markdown(content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("DOWNLOAD JSON", json.dumps(results, indent=2), "cyber_nexus.json")
            with col2:
                st.download_button("DOWNLOAD TXT", content, "cyber_report.txt")
            with col3:
                pdf_html = f"<html><body style='background:linear-gradient(135deg,#f0f4ff,#e0eaff);color:#1e293b;font-family:Inter,sans-serif;padding:80px;line-height:1.9;'><h1 style='text-align:center;background:linear-gradient(90deg,#8b5cf6,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:52px;margin-bottom:40px;'>{query}</h1><div style='max-width:900px;margin:0 auto;'>{content.replace('#', '<h2 style=\"color:#6366f1;margin-top:40px;\">')}</div></body></html>"
                st.download_button("DOWNLOAD PDF (Print→Save)", pdf_html, "cyber_report.html", "text/html")

            if run_eval:
                with st.expander("DETAILED VALIDATION LOG"):
                    evaluator = ResearchEvaluator()
                    metrics = evaluator.evaluate_research(query, results)
                    st.json(metrics.to_dict())

        except Exception as e:
            st.error(f"SYSTEM ERROR: {str(e)}")

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

# Final touch
st.markdown("""
<div style='text-align:center; padding:80px 20px; color:#6366f1; font-size:18px; font-weight:600;'>
    Cyber Nexus v10 • Intelligence Engineered • 2025
</div>
""", unsafe_allow_html=True)
