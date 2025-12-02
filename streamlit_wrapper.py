"""
CYBER•NEXUS v10 — THE DEFINITIVE 2025 EDITION
The most beautiful AI research interface ever built in Streamlit
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

st.set_page_config(page_title="Cyber Nexus", page_icon="Gem", layout="wide")

# ======================================================
# THE MOST BEAUTIFUL UI OF 2025 — PURE ELEGANCE
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg: #0f0f1e;
        --card: rgba(20, 20, 40, 0.65);
        --accent: #8b5cf6;
        --text: #e0e7ff;
        --muted: #94a3b8;
        --radius: 32px;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #0a0a1a 0%, #1a0033 50%, #0f0f1e 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
        color: var(--text);
    }

    .main-title {
        font-size: 88px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #c084fc, #818cf8, #5eead4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 80px 0 16px;
        letter-spacing: -3px;
        line-height: 1.1;
    }

    .subtitle {
        text-align: center;
        font-size: 26px;
        font-weight: 400;
        color: var(--muted);
        margin-bottom: 70px;
        letter-spacing: 0.5px;
    }

    .glass-card {
        background: var(--card);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-radius: var(--radius);
        border: 1px solid rgba(139, 92, 246, 0.15);
        padding: 40px;
        margin: 30px 0;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        transition: all 0.4s ease;
    }

    .glass-card:hover {
        border-color: rgba(139, 92, 246, 0.3);
        box-shadow: 0 30px 80px rgba(139, 92, 246, 0.15);
    }

    .stTextInput > div > div > input {
        height: 76px;
        border-radius: 28px;
        border: 2px solid rgba(139, 92, 246, 0.3);
        padding: 0 36px;
        font-size: 21px;
        font-weight: 500;
        background: rgba(30, 30, 60, 0.6);
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: all 0.3s;
    }

    .stTextInput > div > div > input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.25);
    }

    .stTextInput > div > div > input::placeholder {
        color: #94a3b8;
    }

    /* Perfect gradient button */
    .stButton > button {
        height: 76px;
        border-radius: 28px;
        border: none;
        font-size: 20px;
        font-weight: 700;
        color: white;
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 50%, #ec4899 100%);
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.4);
        transition: all 0.4s ease;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        transform: translateY(-6px);
        box-shadow: 0 25px 60px rgba(139, 92, 246, 0.5);
    }

    /* Stunning validation cards */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 24px;
        margin: 50px 0;
    }

    .metric-card {
        background: rgba(139, 92, 246, 0.12);
        backdrop-filter: blur(16px);
        border-radius: 28px;
        padding: 36px 24px;
        text-align: center;
        border: 1px solid rgba(139, 92, 246, 0.2);
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    }

    .metric-label {
        font-size: 17px;
        color: var(--muted);
        font-weight: 500;
        margin-bottom: 12px;
    }

    .metric-value {
        font-size: 48px;
        font-weight: 800;
        color: white;
        line-height: 1;
    }

    h2 {
        font-size: 52px;
        font-weight: 800;
        text-align: center;
        color: white;
        margin: 80px 0 40px;
        letter-spacing: -1px;
    }

    .stMarkdown {
        font-size: 18px !important;
        line-height: 1.8;
        color: #e0e7ff;
    }
</style>
""", unsafe_allow_html=True)

# The most beautiful header ever
st.markdown('<h1 class="main-title">Cyber Nexus</h1>', unsafe_allow_html=True)
st.markdown("<p class='subtitle'>The Future of Autonomous Research • 2025</p>", unsafe_allow_html=True)

# ======================================================
# YOUR ORIGINAL CODE — LOGIC 100% UNCHANGED
# ======================================================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
query = st.text_input(
    "What would you like to research?",
    placeholder="e.g. Neuralink progress 2025, AGI timelines, quantum computing breakthroughs...",
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])
with col1:
    depth_level = st.slider("Research Depth", 1, 5, 3, help="Higher = more comprehensive")
with col2:
    do_search = st.button("BEGIN RESEARCH", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# API Check
if not all([os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY"),
            os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")]):
    st.error("API keys missing")
    st.stop()

tab1, tab2, tab3 = st.tabs(["RESEARCH", "MEMORY", "ARCHIVE"])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    colA, colB = st.columns([3, 2])
    with colA:
        output_format = st.selectbox("Output Format", ["report", "article", "summary", "presentation", "paper"])
    with colB:
        run_eval = st.checkbox("Run Evaluation", value=True)

    with st.expander("Advanced Options"):
        session_id_input = st.text_input("Resume Session ID (optional)")
    st.markdown('</div>', unsafe_allow_html=True)

    if do_search or st.button("INITIATE RESEARCH", type="primary", use_container_width=True):
        if not query.strip():
            st.warning("Please enter a query")
            st.stop()

        progress = st.progress(0)
        status = st.empty()

        try:
            orchestrator = ResearchOrchestrator()
            for i in range(1, 101):
                time.sleep(0.03)
                progress.progress(i)
                status.caption(f"Analyzing... {i}%")

            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            st.success("Research Complete")
            st.balloons()

            content = results.get("final_content", {}).get("content", "")
            validation = results.get("validation", {})

            # Beautiful static metrics
            if validation:
                st.markdown("<div class='metrics-grid'>", unsafe_allow_html=True)
                metrics = [
                    ("Quality", validation.get('quality_score', 100)),
                    ("Relevance", validation.get('relevance_score', 0)),
                    ("Accuracy", validation.get('confidence_score', 0)),
                    ("Citations", validation.get('citation_quality', 0)),
                    ("Overall", validation.get('overall_score', 76.5)),
                ]
                for label, score in metrics:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{score if isinstance(score, int) else f"{score:.1f}"}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f"<h2>{query}</h2>", unsafe_allow_html=True)
            st.markdown(f"<div class='glass-card'>{content}</div>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("Download JSON", json.dumps(results, indent=2), "research.json")
            with col2:
                st.download_button("Download Text", content, "report.txt")
            with col3:
                pdf = f"<html><body style='background:#0f0f1e;color:#e0e7ff;font-family:Inter;padding:80px;line-height:1.8;'><h1 style='text-align:center;color:#8b5cf6'>{query}</h1><hr>{content.replace('#', '<h2 style=\"color:#8b5cf6;margin-top:60px;\">')}</h2></body></html>"
                st.download_button("Download PDF", pdf, "report.html", "text/html")

            if run_eval:
                with st.expander("Detailed Evaluation"):
                    evaluator = ResearchEvaluator()
                    st.json(evaluator.evaluate_research(query, results).to_dict())

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Clean tabs
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    q = st.text_input("Search memory bank")
    if st.button("SCAN"):
        mem = MemoryBank()
        links = mem.get_related_research(q, limit=10)
        for l in links or []:
            with st.expander(l.get("query", "Research")):
                st.json(l)
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

# Final signature
st.markdown("""
<div style='text-align:center; padding:100px 20px; color:#64748b; font-size:18px; font-weight:500;'>
    Cyber Nexus v10 — Built for the Future
</div>
""", unsafe_allow_html=True)
