"""
CYBER•NEXUS v10 — THE ULTIMATE 2025 EDITION
Now with streamlit-lottie + streamlit-extras + glassmorphism
"""

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_card import card
import requests
import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator
from memory.memory_bank import MemoryBank

# ======================================================
# PAGE CONFIG & BEST UI EVER
# ======================================================
st.set_page_config(page_title="Cyber Nexus", page_icon="Gem", layout="wide")

# Load Lottie animation
@st.cache_data
def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottie("https://assets9.lottiefiles.com/packages/lf20_kkflmtur.json")

# ======================================================
# GORGEOUS CSS — 2025 PREMIUM
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: transparent;
    }
    .big-title {
        font-size: 88px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #a8edea, #fed6e3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 40px 0 10px 0;
        letter-spacing: -3px;
    }
    .subtitle {
        text-align: center;
        font-size: 24px;
        color: rgba(255,255,255,0.85);
        font-weight: 400;
        margin-bottom: 60px;
    }
    .glass {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 32px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 40px;
        margin: 20px 0;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER WITH LOTTIE ANIMATION
# ======================================================
st.markdown('<h1 class="big-title">Cyber Nexus</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Next-Gen Autonomous Research Intelligence</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st_lottie(lottie_ai, height=280, key="ai_brain")

add_vertical_space(3)

# ======================================================
# INPUT CARD
# ======================================================
with st.container():
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    colored_header(
        label="Begin Your Research",
        description="Ask anything — the AI will dive deep",
        color_name="violet-70"
    )
    
    query = st.text_input(
        "What would you like to explore?",
        placeholder="e.g. Neuralink 2025 trials, AGI safety, quantum supremacy...",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([3,1])
    with col1:
        depth_level = st.slider("Research Depth", 1, 5, 3, help="Higher = more thorough")
    with col2:
        st.write("")
        st.write("")
        do_search = st.button("START RESEARCH", use_container_width=True, type="primary")
    
    st.markdown("</div>", unsafe_allow_html=True)

# API check
if not all([os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY"),
            os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")]):
    st.error("API Keys Missing — Check .env or secrets")
    st.stop()

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3 = st.tabs(["RESEARCH", "MEMORY", "ARCHIVE"])

with tab1:
    with st.container():
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3,2])
        with col1:
            output_format = st.selectbox("Format", ["report", "article", "summary", "presentation", "paper"])
        with col2:
            run_eval = st.checkbox("Run Evaluation", value=True)
        
        with st.expander("Advanced"):
            session_id = st.text_input("Resume Session ID")
        
        st.markdown("</div>", unsafe_allow_html=True)

    if do_search or st.button("INITIATE RESEARCH", type="primary", use_container_width=True):
        if not query:
            st.warning("Enter a query first")
            st.stop()

        with st.spinner("Deploying neural agents..."):
            progress = st.progress(0
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
                    session_id=session_id or None
                )
                
                st.success("Research Complete")
                st.balloons()
                
                content = results.get("final_content", {}).get("content", "")
                validation = results.get("validation", {})

                # Beautiful validation using streamlit-extras
                if validation:
                    colored_header("Validation Scores", "", "blue-70")
                    cols = st.columns(len(validation))
                    metrics = [
                        ("Quality", validation.get('quality_score', 100)),
                        ("Relevance", validation.get('relevance_score', 0)),
                        ("Accuracy", validation.get('confidence_score', 0)),
                        ("Citations", validation.get('citation_quality', 0)),
                        ("Overall", validation.get('overall_score', 76.5)),
                    ]
                    for col, (label, score) in zip(cols, metrics):
                        with col:
                            card(
                                title=str(score),
                                text=label,
                                styles={
                                    "card": {
                                        "background": "rgba(139, 92, 246, 0.15)",
                                        "padding": "24px",
                                        "border-radius": "20px",
                                        "text-align": "center",
                                        "box-shadow": "0 10px 30px rgba(0,0,0,0.2)"
                                    },
                                    "text": {"font-size": "18px", "color": "#e0e7ff"},
                                    "title": {"font-size": "42px", "font-weight": "800", "color": "white"}
                                }
                            )

                # Result
                colored_header(f"Research: {query}", "", "violet-70")
                st.markdown(f"<div class='glass'>{content}</div>", unsafe_allow_html=True)

                # Downloads
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.download_button("JSON", json.dumps(results, indent=2), "result.json")
                with c2:
                    st.download_button("Text", content, "report.txt")
                with c3:
                    st.download_button("PDF", f"<h1>{query}</h1>{content}", "report.html", "text/html")

                if run_eval:
                    with st.expander("Detailed Evaluation"):
                        evaluator = ResearchEvaluator()
                        st.json(evaluator.evaluate_research(query, results).to_dict())

            except Exception as e:
                st.error(f"Error: {e}")

# Memory & Archive tabs
with tab2:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    colored_header("Memory Bank", "Search past research", "blue-70")
    q = st.text_input("Search memory")
    if st.button("SCAN"):
        mem = MemoryBank()
        links = mem.get_related_research(q, limit=10)
        for l in links or []:
            with st.expander(l.get("query", "Research")):
                st.json(l)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    colored_header("Archive", "Previous sessions", "green-70")
    out = Path("outputs")
    if out.exists():
        for f in sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)[:20]:
            try:
                data = json.load(open(f))
                with st.expander(data.get("query", "Untitled")):
                    st.json(data)
            except:
                pass
    st.markdown("</div>", unsafe_allow_html=True)

# Final touch
st.markdown("""
<div style='text-align:center; padding:100px 20px; color:rgba(255,255,255,0.7); font-size:18px; text-align:center;'>
    Cyber Nexus v10 — Powered by Intelligence • 2025
</div>
""", unsafe_allow_html=True)
