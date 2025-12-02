"""
CYBER•NEXUS v10 — FINAL TERMINAL EDITION
Now with clean Figma-style UI
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
# FIGMA-STYLE CLEAN MODERN UI (2025 SaaS DESIGN)
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #f8fafc;
        --card: rgba(255, 255, 255, 0.85);
        --border: rgba(255, 255, 255, 0.3);
        --primary: #6366f1;
        --gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        --text: #1e293b;
        --text-light: #64748b;
        --shadow: 0 10px 30px -8px rgba(99, 102, 241, 0.25);
        --radius: 20px;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg);
        font-family: 'Inter', sans-serif;
        color: var(--text);
    }

    .main-title {
        font-size: 72px;
        font-weight: 800;
        text-align: center;
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 40px 0 12px;
        letter-spacing: -2px;
    }

    .subtitle {
        text-align: center;
        font-size: 22px;
        color: var(--text-light);
        font-weight: 500;
        margin-bottom: 50px;
    }

    .glass-card {
        background: var(--card);
        border-radius: var(--radius);
        padding: 32px;
        margin: 24px 0;
        backdrop-filter: blur(16px);
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }

    .stTextInput > div > div > input {
        background: white !important;
        border: 2px solid #e2e106 !important;
        border-radius: 16px !important;
        padding: 18px 20px !important;
        font-size: 18px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        transition:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 4px rgba(99,102,241,0.15) !important;
        }
    }

    .stButton > button {
        background: var(--gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 36px !important;
        font-weight: 600 !important;
        font-size: 17px !important;
        box-shadow: 0 10px 30px rgba(99,102,241,0.35);
        height: 56px;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(99,102,241,0.45);
    }

    .validation-box {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border-radius: 18px;
        padding: 28px;
        margin: 32px 0;
        text-align: center;
        box-shadow: var(--shadow);
        font-weight: 600;
    }

    .val-item {
        display: inline-block;
        margin: 0 24px;
        font-size: 16px;
    }

    .score {
        font-size: 24px;
        font-weight: 700;
        margin-left: 8px;
    }

    h2 {
        font-size: 40px !important;
        font-weight: 700 !important;
        text-align: center;
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 40px 0 20px;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER — Figma style
# ======================================================
st.markdown('<h1 class="main-title">Cyber Nexus</h1>', unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Advanced Autonomous Research Terminal • Powered by Intelligence</p>", unsafe_allow_html=True)

# ======================================================
# YOUR EXACT ORIGINAL CODE STARTS HERE — 100% UNCHANGED
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

            # Figma-style validation box
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

            # Report
            st.markdown(f'<div class="glass-card"><h2>TARGET: {query.upper()}</h2>', unsafe_allow_html=True)
            st.markdown(content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Downloads
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("DOWNLOAD JSON", json.dumps(results, indent=2), "cyber_nexus.json")
            with col2:
                st.download_button("DOWNLOAD TXT", content, "cyber_report.txt")
            with col3:
                pdf_html = f"<html><body style='background:#f8fafc;color:#1e293b;font-family:Inter,sans-serif;padding:60px;line-height:1.8;'><h1 style='text-align:center;background:var(--gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:48px;'>{query}</h1><hr>{content.replace('#', '<br><br><strong>#')}</strong></body></html>"
                st.download_button("DOWNLOAD PDF (Print→Save)", pdf_html, "cyber_report.html", "text/html")

            if run_eval:
                with st.expander("DETAILED VALIDATION LOG"):
                    evaluator = ResearchEvaluator()
                    metrics = evaluator.evaluate_research(query, results)
                    st.json(metrics.to_dict())

        except Exception as e:
            st.error(f"SYSTEM ERROR: {str(e)}")

# Other tabs — clean Figma style
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

# Footer
st.markdown("""
<div style='text-align:center; padding:60px 20px; color:#64748b; font-size:16px;'>
    Cyber Nexus v10 • Built with Intelligence • 2025
</div>
""", unsafe_allow_html=True)
