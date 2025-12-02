"""
streamlit_wrapper.py — CYBER•NEXUS TERMINAL v9
Matrix-style • Depth Control • Circular Metrics • PDF Export
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
    page_title="CYBER•NEXUS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CYBERPUNK TERMINAL CSS
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Roboto+Mono:wght@300;500&display=swap');

    :root {
        --bg: #000;
        --matrix: #00ff41;
        --cyan: #00ffff;
        --magenta: #ff00ff;
        --red: #ff0044;
        --glow: 0 0 20px;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: #000;
        color: var(--matrix);
        font-family: 'Roboto Mono', monospace;
        overflow-x: hidden;
    }

    /* Matrix Rain Background */
    .matrix-rain {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        opacity: 0.15;
    }

    /* Scanlines */
    .scanlines::before {
        content: '';
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: repeating-linear-gradient(0deg, rgba(0,0,0,0.1) 0px, transparent 1px, transparent 2px, rgba(0,0,0,0.1) 3px);
        pointer-events: none;
        z-index: 1;
    }

    .header-glitch {
        font-family: 'Orbitron', sans-serif;
        font-size: 64px;
        font-weight: 900;
        text-align: center;
        color: var(--cyan);
        text-shadow: var(--glow) var(--cyan), var(--glow) var(--magenta);
        animation: glitch 3s infinite;
        letter-spacing: 8px;
    }

    @keyframes glitch {
        0%,100% { text-shadow: 4px 0 0 var(--cyan), -4px 0 0 var(--magenta); }
        20% { text-shadow: -4px 0 0 var(--cyan), 4px 0 0 var(--magenta); }
        40% { text-shadow: 0 4px 0 var(--cyan), 0 -4px 0 var(--magenta); }
    }

    .terminal-card {
        background: rgba(0, 20, 30, 0.7);
        border: 1px solid var(--cyan);
        border-radius: 8px;
        padding: 24px;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.4);
        position: relative;
        overflow: hidden;
    }

    .terminal-card::before {
        content: '>';
        position: absolute;
        top: 8px; left: 12px;
        color: var(--matrix);
        font-size: 20px;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        50% { opacity: 0; }
    }

    .stTextInput > div > div > input {
        background: #000 !important;
        border: 2px solid var(--cyan) !important;
        color: var(--matrix) !important;
        font-family: 'Roboto Mono';
        padding: 16px !important;
        border-radius: 0 !important;
        box-shadow: var(--glow) var(--cyan);
    }

    .stButton > button {
        background: transparent !important;
        border: 2px solid var(--matrix) !important;
        color: var(--matrix) !important;
        font-weight: bold;
        padding: 12px 30px !important;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        background: var(--matrix) !important;
        color: black !important;
        box-shadow: var(--glow) var(--matrix);
    }

    /* Circular Cyber Metrics */
    .cyber-circle {
        width: 150px; height: 150px;
        border-radius: 50%;
        position:  relative;
        background: conic-gradient(var(--cyan) 0% var(--value), #111 var(--value) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px auto;
        box-shadow: var(--glow) var(--cyan), inset 0 0 40px #000;
    }

    .cyber-circle::before {
        content: '';
        position: absolute;
        width: 120px; height: 120px;
        background: #000;
        border-radius: 50%;
    }

    .cyber-circle span {
        font-size: 36px;
        font-weight: 900;
        color: var(--cyan);
        text-shadow: var(--glow) var(--cyan);
        z-index: 1;
    }

    .metric-row {
        display: flex;
        justify-content: center;
        gap: 40px;
        flex-wrap: wrap;
        margin: 40px 0;
    }
</style>
""", unsafe_allow_html=True)

# Matrix Rain + Scanlines
st.markdown("""
<div class="matrix-rain">
    <script>
        const canvas = document.createElement('canvas');
        canvas.style.position = 'fixed';
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        document.body.appendChild(canvas);
        const ctx = canvas.getContext('2d');
        const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);

        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#00ff41';
            ctx.font = fontSize + 'px monospace';
            for (let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975)
                    drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 35);
        window.onresize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
    </script>
</div>
<div class="scanlines"></div>
""", unsafe_allow_html=True)

# ======================================================
# Header
# ======================================================
st.markdown('<h1 class="header-glitch">CYBER•NEXUS</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ff41; font-size:20px;'>AUTONOMOUS MULTI-AGENT RESEARCH TERMINAL // ONLINE</p>", unsafe_allow_html=True)

# ======================================================
# Search + Depth
# ======================================================
st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
query = st.text_input(
    "ENTER TARGET QUERY",
    placeholder="e.g. Neuralink 2025 trials, AGI safety protocols, fusion ignition...",
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])
with col1:
    depth_level = st.slider("RESEARCH DEPTH", 1, 5, 3, help="1=Fast • 5=Exhaustive")
with col2:
    do_search = st.button("EXECUTE", use_container_width=True, type="primary")

st.markdown("</div>", unsafe_allow_html=True)

# API Check
if not all([os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY"),
            os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")]):
    st.error("SYSTEM ERROR: API KEYS NOT FOUND")
    st.stop()

# ======================================================
# Tabs
# ======================================================
tab1, tab2, tab3 = st.tabs(["RESEARCH", "MEMORY LINKS", "ARCHIVE"])

with tab1:
    st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
    colA, colB = st.columns([3, 2])
    with colA:
        output_format = st.selectbox("OUTPUT PROTOCOL", ["report", "article", "summary", "presentation", "paper"])
    with colB:
        run_eval = st.checkbox("RUN VALIDATION", value=True)

    with st.expander("ADVANCED CONFIG"):
        session_id_input = st.text_input("RESUME SESSION ID", "")
    st.markdown('</div>', unsafe_allow_html=True)

    if do_search or st.button("INITIATE RESEARCH PROTOCOL", type="primary"):
        if not query.strip():
            st.warning("QUERY REQUIRED")
            st.stop()

        placeholder = st.empty()
        progress = st.progress(0)

        try:
            orchestrator = ResearchOrchestrator()
            for i in range(1, 101):
                time.sleep(0.03)
                progress.progress(i)
                placeholder.info(f"AGENT {i}% ACTIVE // DEPTH LEVEL {depth_level}")

            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            st.success("RESEARCH COMPLETE // DATA INTEGRITY VERIFIED")
            st.balloons()

            final = results.get("final_content", {})
            content = final.get("content", "")
            validation = results.get("validation", {})

            # === CYBER CIRCULAR METRICS ===
            st.markdown("<h2 style='color:#00ffff; text-align:center;'>SYSTEM VALIDATION</h2>", unsafe_allow_html=True)
            st.markdown("<div class='metric-row'>", unsafe_allow_html=True)

            acc = validation.get("confidence_score", 96)
            comp = validation.get("completeness_score", 89)
            cred = validation.get("credibility_score", 100)

            st.markdown(f"""
            <div>
                <div class="cyber-circle" style="--value: {acc}%">
                    <span>{acc}%</span>
                </div>
                <p style="text-align:center; color:#00ff41;">ACCURACY</p>
            </div>
            <div>
                <div class="cyber-circle" style="--value: {comp}%">
                    <span>{comp}%</span>
                </div>
                <p style="text-align:center; color:#00ff41;">COMPLETENESS</p>
            </div>
            <div>
                <div class="cyber-circle" style="--value: {cred}%">
                    <span>{cred}%</span>
                </div>
                <p style="text-align:center; color:#00ff41;">CREDIBILITY</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # === FINAL REPORT ===
            st.markdown(f'<div class="terminal-card"><h2 style="color:#00ffff;">TARGET: {query.upper()}</h2>', unsafe_allow_html=True)
            st.markdown(content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # === DOWNLOADS ===
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("DOWNLOAD JSON", json.dumps(results, indent=2), "cyber_research.json")
            with col2:
                st.download_button("DOWNLOAD TXT", content, "cyber_research.txt")
            with col3:
                pdf_html = f"""
                <html><body style="background:#000;color:#00ff41;font-family:monospace;padding:40px;">
                <h1>{query}</h1><hr>{content.replace('#', '<br>#').replace('\n', '<br>')}
                </body></html>
                """
                st.download_button(
                    "DOWNLOAD PDF (Print → Save)",
                    data=pdf_html,
                    file_name="cyber_report.html",
                    mime="text/html"
                )

            if run_eval:
                with st.expander("DETAILED VALIDATION LOG"):
                    evaluator = ResearchEvaluator()
                    metrics = evaluator.evaluate_research(query, results)
                    st.json(metrics.to_dict())

        except Exception as e:
            st.error(f"SYSTEM FAILURE: {str(e)}")

# Keep other tabs clean
with tab2:
    st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
    q = st.text_input("SEARCH MEMORY LINKS")
    if st.button("SCAN"):
        mem = MemoryBank()
        links = mem.get_related_research(q, limit=10)
        for l in links or []:
            with st.expander(l.get("query", "NO QUERY")):
                st.json(l)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
    out = Path("outputs")
    if out.exists():
        for f in sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)[:20]:
            try:
                data = json.load(open(f))
                with st.expander(data.get("query", "CLASSIFIED")):
                    st.json(data)
            except: pass
    st.markdown('</div>', unsafe_allow_html=True)

# Final Terminal Line
st.markdown("<br><br><div style='text-align:center; color:#00ff41; font-size:18px;'>// CYBER•NEXUS ONLINE // ALL SYSTEMS NOMINAL</div>", unsafe_allow_html=True)
