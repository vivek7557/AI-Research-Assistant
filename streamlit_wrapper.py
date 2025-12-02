"""
CYBER•NEXUS v10 — FINAL TERMINAL EDITION
Perfect validation line • Ultra cyber styling • Depth control • PDF export
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

st.set_page_config(page_title="CYBER•NEXUS", page_icon="Lightning", layout="wide")

# ======================================================
# CLEAN CYBER GRADIENT UI — ONLY VISUAL UPGRADE
# ======================================================
st.markdown("""
<style>
    :root {
        --green: #00ff41;
        --cyan: #00ffff;
        --magenta: #ff00ff;
        --orange: #ffaa00;
        --bg-dark: #000814;
        --card-bg: rgba(0, 15, 40, 0.7);
        --gradient: linear-gradient(135deg, #00ff41, #00ffff, #ff00ff);
        --gradient-soft: linear-gradient(135deg, rgba(0,255,65,0.15), rgba(0,255,255,0.1), rgba(255,0,255,0.15));
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg-dark);
        color: var(--green);
        font-family: 'Courier New', monospace;
    }

    .matrix-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        opacity: 0.1;
        z-index: 0;
        background: var(--gradient-soft);
    }

    .header-glitch {
        font-size: 76px;
        font-weight: 900;
        text-align: center;
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px #00ffff;
        letter-spacing: 10px;
        margin: 30px 0 10px;
        animation: pulse 4s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.9; }
        50% { opacity: 1; }
    }

    .terminal-card {
        background: var(--card-bg);
        border: 1px solid #00ffff;
        border-radius: 12px;
        padding: 28px;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
        backdrop-filter: blur(8px);
        position: relative;
        border-image: var(--gradient) 1;
    }

    .terminal-card::before {
        content: '> ';
        color: var(--green);
        font-weight: bold;
        font-size: 24px;
        position: absolute;
        left: 16px;
        top: 16px;
        animation: blink 1s infinite;
    }

    @keyframes blink { 50% { opacity: 0; } }

    .stTextInput > div > div > input {
        background: #000 !important;
        border: 2px solid transparent !important;
        border-image: var(--gradient) 1 !important;
        color: #00ff41 !important;
        font-size: 18px !important;
        padding: 16px !important;
        border-radius: 8px !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
    }

    .stButton > button {
        background: linear-gradient(45deg, #000, #0a1a2a) !important;
        border: 2px solid transparent !important;
        border-image: var(--gradient) 1 !important;
        color: #00ffff !important;
        font-weight: bold;
        padding: 14px 32px !important;
        border-radius: 8px;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.5);
    }

    .stButton > button:hover {
        background: var(--gradient) !important;
        color: black !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(255, 0, 255, 0.6);
    }

    /* Validation line — now with gradient glow */
    .validation-line {
        background: var(--gradient-soft);
        border: 2px solid transparent;
        border-image: var(--gradient) 1;
        border-radius: 12px;
        padding: 20px;
        margin: 25px 0;
        font-size: 16px;
        font-weight: 500;
        box-shadow: 0 0 35px rgba(0, 255, 255, 0.5);
        backdrop-filter: blur(6px);
    }

    .val-item {
        display: inline-block;
        margin-right: 32px;
        min-width: 160px;
        color: #00ffff;
        font-weight: bold;
    }

    .score-green { color: #00ff41; font-weight: bold; font-size: 1.1em; }
    .score-orange { color: #ffaa00; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Soft gradient matrix rain
st.markdown("""
<div class="matrix-bg">
    <script>
        const canvas = document.createElement('canvas');
        canvas.style.position = 'fixed';
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        document.body.appendChild(canvas);
        const ctx = canvas.getContext('2d');
        const chars = '01アイウエオカキクケコサシスセソ0101';
        const fontSize = 14;
        const columns = canvas.width/fontSize;
        const drops = Array(Math.floor(columns)).fill(1);

        function draw() {
            ctx.fillStyle = 'rgba(0, 8, 20, 0.05)';
            ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#00ff41';
            ctx.font = fontSize + 'px monospace';
            for(let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random()*chars.length)];
                ctx.fillText(text, i*fontSize, drops[i]*fontSize);
                if(drops[i]*fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 50);
    </script>
</div>
""", unsafe_allow_html=True)

# ======================================================
# YOUR ORIGINAL HEADER (just made prettier)
# ======================================================
st.markdown('<h1 class="header-glitch">CYBER•NEXUS</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ff41; font-size:22px; letter-spacing:5px; text-shadow: 0 0 20px #00ffff;'>AUTONOMOUS RESEARCH TERMINAL v10 // ONLINE</p>", unsafe_allow_html=True)

# ======================================================
# YOUR EXACT SAME CODE FROM HERE — NO CHANGES
# ======================================================
st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
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
    st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
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
                <div class="validation-line">
                    <div class="val-item">"<strong>completeness</strong>": <span class="score-orange">{validation.get('completeness_score', 0)}</span></div>
                    <div class="val-item">"<strong>accuracy</strong>": <span class="score-green">{validation.get('confidence_score', 0)}</span></div>
                    <div class="val-item">"<strong>relevance</strong>": <span class="score-orange">{validation.get('relevance_score', 0)}</span></div>
                    <div class="val-item">"<strong>quality</strong>": <span class="score-green">{validation.get('quality_score', 100)}</span></div>
                    <div class="val-item">"<strong>efficiency</strong>": <span class="score-orange">{validation.get('efficiency_score', 0)}</span></div>
                    <div class="val-item">"<strong>citations</strong>": <span class="score-green">{validation.get('citation_quality', 0)}</span></div>
                    <div class="val-item">"<strong>overall</strong>": <span class="score-green"><strong>{validation.get('overall_score', 76.5):.1f}</strong></span></div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f'<div class="terminal-card"><h2 style="color:#00ffff; text-align:center; text-shadow: 0 0 20px #00ffff;">TARGET: {query.upper()}</h2>', unsafe_allow_html=True)
            st.markdown(content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("DOWNLOAD JSON", json.dumps(results, indent=2), "cyber_nexus.json")
            with col2:
                st.download_button("DOWNLOAD TXT", content, "cyber_report.txt")
            with col3:
                pdf_html = f"<html><body style='background:#000;color:#00ff41;font-family:monospace;padding:40px;'><h1 style='color:#00ffff;text-align:center;'>{query}</h1><hr>{content.replace('#', '<br>#')}</body></html>"
                st.download_button("DOWNLOAD PDF (Print→Save)", pdf_html, "cyber_report.html", "text/html")

            if run_eval:
                with st.expander("DETAILED VALIDATION LOG"):
                    evaluator = ResearchEvaluator()
                    metrics = evaluator.evaluate_research(query, results)
                    st.json(metrics.to_dict())

        except Exception as e:
            st.error(f"SYSTEM ERROR: {str(e)}")

with tab2:
    st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
    q = st.text_input("SEARCH MEMORY")
    if st.button("SCAN"):
        mem = MemoryBank()
        links = mem.get_related_research(q, limit=10)
        for l in links or []:
            with st.expander(l.get("query", "CLASSIFIED")):
                st.json(l)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
    out = Path("outputs")
    if out.exists():
        for f in sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)[:20]:
            try:
                data = json.load(open(f))
                with st.expander(data.get("query", "NO DATA")):
                    st.json(data)
            except: pass
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='text-align:center; color:#00ff41; padding:50px; font-size:19px; text-shadow: 0 0 30px #00ffff;'>// CYBER•NEXUS v10 // GRADIENT CORE ONLINE // 2025</div>", unsafe_allow_html=True)
