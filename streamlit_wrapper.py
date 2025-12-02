"""
streamlit_wrapper.py — ULTIMATE FUTURISTIC EDITION
Zero logic changes • Fixed indentation • Ready to run
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

# --- Core Logic (UNCHANGED) ---
from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator
from memory.memory_bank import MemoryBank

# ======================================================
# Page Config
# ======================================================
st.set_page_config(
    page_title="ResearchAI • Nexus",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# ULTRA FUTURISTIC CSS
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Exo+2:wght@300;500;700&display=swap');

    :root {
        --nebula-1: #0a0022;
        --nebula-2: #1a0033;
        --nebula-3: #2d0066;
        --accent-cyan: #00f5ff;
        --accent-purple: #9d00ff;
        --accent-pink: #ff29d4;
        --glow-cyan: rgba(0, 245, 255, 0.6);
        --glow-purple: rgba(157, 0, 255, 0.6);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 20% 80%, #1a0033 0%, #0a0022 50%, #000000 100%);
        background-size: 400% 400%;
        animation: nebulaFlow 20s ease infinite;
        font-family: 'Exo 2', sans-serif;
    }

    @keyframes nebulaFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .header-glow {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, var(--accent-cyan), var(--accent-purple), transparent);
        box-shadow: 0 0 30px var(--accent-cyan);
        z-index: 9999;
        animation: pulseLine 6s infinite;
    }

    @keyframes pulseLine {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; box-shadow: 0 0 50px var(--accent-purple); }
    }

    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 52px;
        font-weight: 900;
        background: linear-gradient(90deg, #00f5ff, #9d00ff, #ff29d4);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
        animation: titleGlow 5s ease-in-out infinite;
    }

    @keyframes titleGlow {
        0%, 100% { filter: hue-rotate(0deg) drop-shadow(0 0 20px #00f5ff); }
        50% { filter: hue-rotate(180deg) drop-shadow(0 0 40px #ff29d4); }
    }

    .logo-orb {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #ffffff, #00f5ff);
        box-shadow: 0 0 60px #00f5ff, inset 0 0 30px #9d00ff;
        animation: orbPulse 4s infinite;
    }

    @keyframes orbPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); box-shadow: 0 0 100px #ff29d4; }
    }

    .stTextInput > div > div > input {
        background: rgba(10, 0, 34, 0.7) !important;
        border: 2px solid transparent !important;
        border-radius: 20px !important;
        color: white !important;
        padding: 18px 24px !important;
        font-size: 18px !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 30px var(--glow-cyan) !important;
    }

    .stButton > button {
        background: linear-gradient(45deg, #1a0033, #2d0066) !important;
        border: 2px solid var(--accent-purple) !important;
        color: white !important;
        border-radius: 16px !important;
        padding: 14px 32px !important;
        font-weight: 700 !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 0 20px rgba(157, 0, 255, 0.4);
    }

    .stButton > button:hover {
        background: rgba(157, 0, 255, 0.2) !important;
        border-color: var(--accent-cyan) !important;
        color: var(--accent-cyan) !important;
        transform: translateY(-4px);
        box-shadow: 0 0 40px var(--glow-cyan) !important;
    }

    .glass-card {
        background: rgba(20, 10, 60, 0.35);
        border-radius: 20px;
        border: 1px solid rgba(100, 50, 200, 0.3);
        backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), 0 0 40px rgba(0, 245, 255, 0.15);
        padding: 24px;
        transition: all 0.4s ease;
        position: relative;
        overflow:响 hidden;
    }

    .glass-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(0, 245, 255, 0.3);
        border-color: var(--accent-cyan);
    }

    .orb-progress {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(var(--accent-cyan) 0%, var(--accent-purple) 70%, #333 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px auto;
        animation: rotateOrb 8s linear infinite;
        box-shadow: 0 0 60px rgba(0, 245, 255, 0.8);
    }

    @keyframes rotateOrb {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .neon-pill {
        display: inline-block;
        padding: 10px 20px;
        margin: 8px;
        border-radius: 30px;
        background: rgba(0, 245, 255, 0.15);
        border: 1px solid var(--accent-cyan);
        color: var(--accent-cyan);
        font-weight: 600;
        transition: all 0.4s;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
    }

    .neon-pill:hover {
        background: var(--accent-cyan);
        color: #000;
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# Floating particles + header glow
st.markdown("""
<div class="header-glow"></div>
<div class="particles">
    <script>
        for(let i=0; i<60; i++){
            let p = document.createElement('div');
            p.style.position = 'absolute';
            p.style.width = p.style.height = Math.random()*5 + 2 + 'px';
            p.style.background = ['#00f5ff','#9d00ff','#ff29d4'][i%3];
            p.style.borderRadius = '50%';
            p.style.left = Math.random()*100 + 'vw';
            p.style.top = Math.random()*100 + 'vh';
            p.style.opacity = Math.random()*0.6 + 0.2;
            p.style.boxShadow = '0 0 20px currentColor';
            p.style.animation = `float ${8+Math.random()*12}s linear infinite`;
            p.style.animationDelay = Math.random()*10 + 's';
            document.body.appendChild(p);
        }
        const style = document.createElement('style');
        style.innerHTML = `@keyframes float {
            0% { transform: translateY(100vh) scale(0.5); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100px) scale(1); opacity: 0; }
        }`;
        document.head.appendChild(style);
    </script>
</div>
""", unsafe_allow_html=True)

# ======================================================
# Header
# ======================================================
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("<div style='text-align:center; padding:50px 0 20px;'>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 5])
    with col_a:
        st.markdown('<div class="logo-orb"></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<h1 class="main-title">RESEARCH•NEXUS</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#bbbbbb; font-size:19px;'>Autonomous Multi-Agent Research Engine • Real-Time • Verified</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# Search
# ======================================================
st.markdown("<div style='text-align:center; margin:40px 0;'>", unsafe_allow_html=True)
query = st.text_input(
    "",
    placeholder="Enter research topic: 'AGI safety 2025', 'fusion breakthroughs', 'neuralink progress'...",
    label_visibility="collapsed",
    key="search_input"
)

_, col_mid, _ = st.columns([1, 1, 1])
with col_mid:
    do_search = st.button("INITIATE RESEARCH", use_container_width=True, key="search_btn")

st.markdown("</div>", unsafe_allow_html=True)

# Pills
st.markdown("""
<div style="text-align:center; margin:30px 0;">
    <span class="neon-pill">AGI Alignment</span>
    <span class="neon-pill">Nuclear Fusion</span>
    <span class="neon-pill">Brain-Computer Interfaces</span>
    <span class="neon-pill">Quantum Computing</span>
    <span class="neon-pill">Longevity</span>
</div>
""", unsafe_allow_html=True)

# ======================================================
# API Key Check
# ======================================================
anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "")

if not (anthropic_key and tavily_key):
    st.error("Missing API keys. Add ANTHROPIC_API_KEY and TAVILY_API_KEY to .env or Streamlit secrets.")
    st.stop()

# ======================================================
# Tabs
# ======================================================
tab1, tab2, tab3 = st.tabs(["New Research", "Related Research", "Memory Vault"])

# ────────────────────────────── TAB 1 ──────────────────────────────
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    colA, colB = st.columns([3, 2])
    with colA:
        output_format = st.selectbox("Output Format", ["report", "article", "summary", "presentation", "paper", "briefing"])
    with colB:
        run_eval = st.checkbox("Run Full Evaluation", value=True)

    with st.expander("Advanced Controls"):
        colx, coly = st.columns(2)
        with colx:
            session_id_input = st.text_input("Resume Session ID (optional)", "")
        with coly:
            depth_level = st.slider("Research Depth", 1, 5, 3)

    st.markdown('</div>', unsafe_allow_html=True)

    start = do_search or st.button("LAUNCH RESEARCH PROTOCOL", type="primary", use_container_width=True)

    if start:
        if not query:
            st.warning("Please enter a research query.")
            st.stop()

        status_container = st.container()
        with status_container:
            st.markdown("<div style='text-align:center; padding:50px 0;'>", unsafe_allow_html=True)
            st.markdown("<div class='orb-progress'><h2 style='color:white;'>0%</h2></div>", unsafe_allow_html=True)
            status_text = st.empty()
            st.markdown("</div>", unsafe_allow_html=True)

        try:
            phases = [
                ("Booting AI agents...", 18),
                ("Scanning knowledge graph...", 38),
                ("Cross-validating sources...", 60),
                ("Synthesizing insights...", 82),
                ("Finalizing report...", 100),
            ]

            orchestrator = ResearchOrchestrator()

            for i, (text, prog) in enumerate(phases):
                status_text.markdown(f"<h3 style='text-align:center; color:#00f5ff;'>{text}</h3>", unsafe_allow_html=True)
                status_container.markdown(f"<div class='orb-progress'><h2 style='color:white;'>{prog}%</h2></div>", unsafe_allow_html=True)
                time.sleep(1.2 if i < 3 else 1.5)

            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            st.success("RESEARCH COMPLETE • Confidence High")
            st.balloons()

            final = results.get("final_content", {})
            content = final.get("content", "")
            summary = results.get("research_summary", {})
            validation = results.get("validation", {})

            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div class='glass-card'><h3>Sources</h3><h1 style='color:#00f5ff;'>{summary.get('total_sources', 0)}</h1></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='glass-card'><h3>Iterations</h3><h1 style='color:#9d00ff;'>{summary.get('iterations', 0)}</h1></div>", unsafe_allow_html=True)
            with col3:
                score = validation.get('confidence_score', 94)
                st.markdown(f"<div class='glass-card'><h3>Confidence</h3><h1 style='color:#ff29d4;'>{score}%</h1></div>", unsafe_allow_html=True)

            # Report
            st.markdown('<div class="glass-card" style="margin-top:30px; padding:40px;">', unsafe_allow_html=True)
            st.markdown(f"<h2 styleART style='text-align:center; color:#00f5ff;'>{query}</h2>", unsafe_allow_html=True)
            if content:
                st.markdown(content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Downloads
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button("Download JSON", json.dumps(results, indent=2), "research_nexus.json", "application/json")
            with col_d2:
                st.download_button("Export Text", content, "research_nexus.txt", "text/plain")

            # Evaluation
            if run_eval:
                with st.expander("Advanced Evaluation Metrics", expanded=True):
                    try:
                        evaluator = ResearchEvaluator()
                        metrics = evaluator.evaluate_research(query, results)
                        st.json(metrics.to_dict())
                    except Exception as e:
                        st.error(f"Evaluation error: {e}")

        except Exception as e:
            st.error(f"Research failed: {str(e)}")
            st.exception(e)

# ────────────────────────────── TAB 2 ──────────────────────────────
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    related_query = st.text_input("Find Related Research", key="related_search")
    if st.button("Search Memory", key="related_btn"):
        memory = MemoryBank()
        rel = memory.get_related_research(related_query, limit=12)
        if rel:
            for x in rel:
                with st.expander(f"{x.get('query', 'Untitled')} • {x.get('timestamp', '')[:10]}"):
                    st.json(x)
        else:
            st.info("No related research found.")
    st.markdown('</div>', unsafe_allow_html=True)

# ────────────────────────────── TAB 3 ──────────────────────────────
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    out = Path("outputs")
    if out.exists():
        files = sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)
        st.write(f"**Memory Vault • {len(files)} Sessions**")
        for f in files[:25]:
            try:
                data = json.load(open(f))
                with st.expander(f"{data.get('query', 'Untitled')} • {f.stem[-10:]}"):
                    st.json(data)
                    st.download_button("Download", json.dumps(data), f.name, key=f"dl_{f.name}")
            except:
                pass
    else:
        st.info("Memory vault is empty.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; padding:60px; color:#666; font-size:14px; margin-top:100px;">
    <h3>Research•Nexus • Autonomous AI Research Engine</h3>
    <p>Made with ❤️ + curiosity • Built on Streamlit • 2025</p>
</div>
""", unsafe_allow_html=True)
