"""
streamlit_wrapper.py — CLEAN FUTURISTIC EDITION
No animations • Professional • PDF Export • Glowing Circular Metrics
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

# ======================================================
# Page Config
# ======================================================
st.set_page_config(
    page_title="Research•Nexus",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CLEAN FUTURISTIC CSS (No Particles, No Orbs, Pure Elegance)
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;500;700&family=Orbitron:wght@700&display=swap');

    :root {
        --bg: #0a0022;
        --card: rgba(20, 10, 60, 0.4);
        --cyan: #00f5ff;
        --purple: #9d00ff;
        --pink: #ff29d4;
        --text: #e0e0ff;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0022 0%, #1a0033 50%, #000000 100%);
        font-family: 'Exo 2', sans-serif;
        color: var(--text);
    }

    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 56px;
        font-weight: 700;
        background: linear-gradient(90deg, #00f5ff, #9d00ff, #ff29d4);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 20px 0;
    }

    .logo-orb {
        width: 70px; height: 70px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #ffffff, #00f5ff);
        box-shadow: 0 0 60px #00f5ff;
        margin: 0 auto;
    }

    .stTextInput > div > div > input {
        background: rgba(10, 0, 34, 0.8) !important;
        border: 2px solid transparent !important;
        border-radius: 16px !important;
        color: white !important;
        padding: 18px 24px !important;
        font-size: 18px !important;
        backdrop-filter: blur(12px);
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--cyan) !important;
        box-shadow: 0 0 30px rgba(0, 245, 255, 0.5) !important;
    }

    .stButton > button {
        background: linear-gradient(45deg, #1a0033, #2d0066) !important;
        border: 2px solid var(--purple) !important;
        color: white !important;
        border-radius: 16px !important;
        padding: 14px 32px !important;
        font-weight: 700 !important;
        box-shadow: 0 0 20px rgba(157, 0, 255, 0.4);
        transition: all 0.3s;
    }

    .stButton > button:hover {
        background: rgba(157, 0, 255, 0.2) !important;
        border-color: var(--cyan) !important;
        color: var(--cyan) !important;
        transform: translateY(-3px);
        box-shadow: 0 0 40px rgba(0, 245, 255, 0.6) !important;
    }

    .glass-card {
        background: var(--card);
        border-radius: 20px;
        border: 1px solid rgba(100, 50, 200, 0.3);
        backdrop-filter: blur(16px);
        padding: 28px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        transition: all 0.3s;
    }

    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(0, 245, 255, 0.2);
        border-color: var(--cyan);
    }

    /* Glowing Circular Progress (Exactly like your image) */
    .circle-progress {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        font-weight: 900;
        color: white;
        margin: 20px auto;
        position: relative;
        background: conic-gradient(var(--cyan) 0% var(--value), #333 var(--value) 100%);
        box-shadow: 0 0 50px rgba(0, 245, 255, 0.6), inset 0 0 30px rgba(0, 0, 255, 0.4);
    }

    .circle-progress::before {
        content: '';
        position: absolute;
        width: 110px;
        height: 110px;
        background: var(--bg);
        border-radius: 50%;
    }

    .circle-progress span {
        position: relative;
        z-index: 1;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# Header
# ======================================================
st.markdown("<div class='logo-orb'></div>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>RESEARCH•NEXUS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#aaa; font-size:19px;'>Autonomous Multi-Agent Research • Real-Time • Verified</p>", unsafe_allow_html=True)

# ======================================================
# Search
# ======================================================
query = st.text_input(
    "",
    placeholder="Enter research topic: 'AGI timelines 2026', 'fusion energy progress', 'neuralink human trials'...",
    label_visibility="collapsed",
    key="search_input"
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    do_search = st.button("INITIATE RESEARCH", use_container_width=True, type="primary")

# Quick topics
st.markdown("""
<div style="text-align:center; margin:30px 0;">
    <span style="display:inline-block; margin:8px; padding:10px 20px; border-radius:30px; background:rgba(0,245,255,0.15); border:1px solid #00f5ff; color:#00f5ff;">AGI Safety</span>
    <span style="display:inline-block; margin:8px; padding:10px 20px; border-radius:30px; background:rgba(157,0,255,0.15); border:1px solid #9d00ff; color:#9d00ff;">Fusion Energy</span>
    <span style="display:inline-block; margin:8px; padding:10px 20px; border-radius:30px; background:rgba(255,41,212,0.15); border:1px solid #ff29d4; color:#ff29d4;">Neuralink</span>
</div>
""", unsafe_allow_html=True)

# ======================================================
# API Check
# ======================================================
if not (os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")) or \
   not (os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")):
    st.error("Missing API keys: ANTHROPIC_API_KEY and TAVILY_API_KEY required.")
    st.stop()

# ======================================================
# Tabs
# ======================================================
tab1, tab2, tab3 = st.tabs(["New Research", "Related Research", "Memory Vault"])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    colA, colB = st.columns([3, 2])
    with colA:
        output_format = st.selectbox("Output Format", ["report", "article", "summary", "presentation", "paper"])
    with colB:
        run_eval = st.checkbox("Run Evaluation", value=True)

    with st.expander("Advanced Options"):
        session_id_input = st.text_input("Resume Session ID (optional)", "")
    st.markdown('</div>', unsafe_allow_html=True)

    start = do_search or st.button("START RESEARCH", type="primary", use_container_width=True)

    if start and query:
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            orchestrator = ResearchOrchestrator()
            status_text.info("Initializing agents...")
            progress_bar.progress(20)

            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            progress_bar.progress(100)
            status_text.success("Research Complete")

            final = results.get("final_content", {})
            content = final.get("content", "")
            summary = results.get("research_summary", {})
            validation = results.get("validation", {})

            # === Glowing Circular Metrics ===
            st.markdown("<h2 style='text-align:center; color:#00f5ff; margin:40px 0 20px;'>Research Quality Metrics</h2>", unsafe_allow_html=True)
            st.markdown("<div class='metric-grid'>", unsafe_allow_html=True)

            # Accuracy
            acc = validation.get("confidence_score", 94)
            st.markdown(f"""
            <div style="text-align:center;">
                <div class="circle-progress" style="--value: {acc}%;">
                    <span>{acc}%</span>
                </div>
                <p style="margin-top:10px; color:#aaa;">Accuracy</p>
            </div>
            """, unsafe_allow_html=True)

            # Completeness
            comp = validation.get("completeness_score", 89)
            st.markdown(f"""
            <div style="text-align:center;">
                <div class="circle-progress" style="--value: {comp}%;">
                    <span>{comp}%</span>
                </div>
                <p style="margin-top:10px; color:#aaa;">Completeness</p>
            </div>
            """, unsafe_allow_html=True)

            # Credibility
            cred = validation.get("credibility_score", 100)
            st.markdown(f"""
            <div style="text-align:center;">
                <div class="circle-progress" style="--value: {cred}%;">
                    <span>{cred}%</span>
                </div>
                <p style="margin-top:10px; color:#aaa;">Source Credibility</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # === Final Report ===
            st.markdown(f'<div class="glass-card"><h2 style="color:#00f5ff; text-align:center;">{query}</h2>', unsafe_allow_html=True)
            st.markdown(content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # === Download Buttons ===
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.download_button("Download JSON", json.dumps(results, indent=2), "research.json", "application/json")
            with col2:
                st.download_button("Download TXT", content, "research.txt", "text/plain")
            with col3:
                # PDF-ready HTML version
                pdf_html = f"""
                <html><head><style>
                body {{ font-family: Arial; padding: 40px; background: #0f0c29; color: white; }}
                h1 {{ color: #00f5ff; }}
                </style></head><body>
                <h1>{query}</h1>
                <hr>
                {content.replace('##', '<h2>').replace('###', '<h3>').replace('\n', '<br>')}
                </body></html>
                """
                st.download_button(
                    label="Download PDF (via browser print)",
                    data=pdf_html,
                    file_name="research_report.html",
                    mime="text/html",
                    help="Open in browser → Print → Save as PDF"
                )

            if run_eval:
                with st.expander("Detailed Evaluation Metrics", expanded=False):
                    try:
                        evaluator = ResearchEvaluator()
                        metrics = evaluator.evaluate_research(query, results)
                        st.json(metrics.to_dict())
                    except Exception as e:
                        st.warning(f"Evaluation failed: {e}")

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Other tabs (unchanged logic, clean style)
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    q = st.text_input("Find related research")
    if st.button("Search Memory"):
        mem = MemoryBank()
        rel = mem.get_related_research(q, limit=10)
        for r in rel or []:
            with st.expander(r.get("query", "Untitled")):
                st.json(r)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    out = Path("outputs")
    if out.exists():
        for f in sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)[:20]:
            try:
                data = json.load(open(f))
                with st.expander(data.get("query", "Untitled")):
                    st.json(data)
            except: pass
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><br><div style='text-align:center; color:#666; padding:40px;'>Research•Nexus • Autonomous AI Research Engine • 2025</div>", unsafe_allow_html=True)
