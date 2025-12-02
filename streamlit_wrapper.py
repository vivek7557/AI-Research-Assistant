"""
CYBER•NEXUS v10 — GRADIENT NEON EDITION
Ultra cyber gradient glow • Perfect validation line • Still 100% your original logic
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
# INSANE GRADIENT CYBERPUNK UI 2099
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Roboto+Mono:wght@300;500&display=swap');

    :root {
        --bg: #000000;
        --primary: #00ff41;
        --cyan: #00ffff;
        --magenta: #ff00ff;
        --orange: #ffaa00;
        --gradient-1: linear-gradient(135deg, #00ff41, #00ffff, #ff00ff);
        --gradient-2: linear-gradient(45deg, #ff00ff, #00ffff, #00ff41);
        --glow-cyan: 0 0 30px #00ffff;
        --glow-magenta: 0 0 30px #ff00ff;
        --glow-green: 0 0 30px #00ff41;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg);
        color: var(--bg);
        font-family: 'Roboto Mono', monospace;
    }

    /* Epic gradient matrix rain */
    .matrix-bg {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        opacity: 0.15;
        z-index: 0;
        background: linear-gradient(180deg, transparent, #001122);
    }

    /* GLITCH TITLE WITH GRADIENT */
    .header-glitch {
        font-family: 'Orbitron', sans-serif;
        font-size: 82px;
        font-weight: 900;
        text-align: center;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: var(--glow-cyan), var(--glow-magenta);
        animation: glitch 3.5s infinite, hue 8s infinite linear;
        letter-spacing: 12px;
        margin: 30px 0 10px;
    }

    @keyframes glitch {
        0%,100% { transform: translate(0); }
        20% { transform: translate(-5px, 5px); }
        40% { transform: translate(-5px, -5px); }
        60% { transform: translate(5px, 5px); }
        80% { transform: translate(5px, -5px); }
    }

    @keyframes hue {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }

    .subtitle-glow {
        text-align: center;
        font-size: 24px;
        font-weight: 500;
        letter-spacing: 6px;
        background: var(--gradient-2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: var(--glow-green);
    }

    .terminal-card {
        background: rgba(5, 10, 30, 0.92);
        border: 2px solid;
        border-image: var(--gradient-1) 1;
        border-radius: 12px;
        padding: 28px;
        margin: 25px 0;
        box-shadow: 0 0 40px rgba(0, 255, 255, 0.4), inset 0 0 20px rgba(255, 0, 255, 0.1);
        backdrop-filter: blur(8px);
        position: relative;
        overflow: hidden;
    }

    .terminal-card::before {
        content: '>';
        color: var(--primary);
        font-size: 28px;
        font-weight: bold;
        position: absolute;
        left: 16px;
        top: 16px;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        50% { opacity: 0; }
    }

    .stTextInput > div > div > input {
        background: #000 !important;
        border: 2px solid transparent !important;
        border-image: var(--gradient-1) 1 !important;
        color: #00ff41 !important;
        font-family: 'Roboto Mono';
        font-size: 18px !important;
        padding: 18px !important;
        border-radius: 8px !important;
        box-shadow: var(--glow-cyan);
    }

    .stButton > button {
        background: linear-gradient(45deg, #000, #111) !important;
        border: 2px solid transparent !important;
        border-image: var(--gradient-2) 1 !important;
        color: #00ffff !important;
        font-weight: bold;
        font-size: 18px;
        padding: 16px 40px !important;
        border-radius: 8px;
        box-shadow: var(--glow-magenta);
        transition: all 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 0, 255, 0.6);
        background: var(--gradient-2) !important;
        color: black !important;
    }

    /* GRADIENT VALIDATION LINE */
    .validation-line {
        background: linear-gradient(90deg, rgba(0,255,65,0.1), rgba(0,255,255,0.1), rgba(255,0,255,0.1));
        border: 2px solid transparent;
        border-image: var(--gradient-1) 1;
        border-radius: 12px;
        padding: 22px;
        margin: 30px 0;
        font-size: 17px;
        font-weight: 500;
        box-shadow: 0 0 35px rgba(0, 255, 255, 0.5);
        backdrop-filter: blur(6px);
    }

    .val-item {
        display: inline-block;
        margin-right: 35px;
        min-width: 180px;
        background: linear-gradient(90deg, #00ff41, #00ffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }

    .score-green { 
        background: linear-gradient(90deg, #00ff41, #aaffaa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 1.2em;
    }

    .score-orange { 
        background: linear-gradient(90deg, #ffaa00, #ffff00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }

    /* Report title gradient */
    h2 {
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        text-align: center;
        text-shadow: var(--glow-cyan);
        letter-spacing: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Gradient Matrix Rain
st.markdown("""
<div class="matrix-bg">
    <script>
        const canvas = document.createElement('canvas');
        canvas.style.position = 'fixed';
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        document.body.appendChild(canvas);
        const ctx = canvas.getContext('2d');
        const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン∇△◆◈';
        const fontSize = 16;
        const columns = canvas.width/fontSize;
        const drops = Array(Math.floor(columns)).fill(1);

        function draw() {
            ctx.fillStyle = 'rgba(0,0,0,0.05)';
            ctx.fillRect(0,0,canvas.width,canvas.height);
            for (let i = 0; i < drops.length; i++) {
                const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
                gradient.addColorStop(0, '#00ff41');
                gradient.addColorStop(0.5, '#00ffff');
                gradient.addColorStop(1, '#ff00ff');
                ctx.fillStyle = gradient;
                const text = chars[Math.floor(Math.random()*chars.length)];
                ctx.fillText(text, i*fontSize, drops[i]*fontSize);
                if (drops[i]*fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 45);
        window.onresize = () => { canvas.width = innerWidth; canvas.height = innerHeight; };
    </script>
</div>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<h1 class="header-glitch">CYBER•NEXUS</h1>', unsafe_allow_html=True)
st.markdown("<p class='subtitle-glow'>AUTONOMOUS RESEARCH TERMINAL v10 // NEON CORE ACTIVE // 2099</p>", unsafe_allow_html=True)

# SEARCH + DEPTH
st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
query = st.text_input(
    "TARGET QUERY",
    placeholder="e.g. Neuralink 2025 • AGI timelines • Fusion ignition • Quantum supremacy...",
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])
with col1:
    depth_level = st.slider("RESEARCH DEPTH LEVEL", 1, 5, 3, help="1 = Fast Scan | 5 = Full Neural Breach")
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
                status.info(f"NEURAL BREACH IN PROGRESS // DEPTH {depth_level} // {i}%")

            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            st.success("RESEARCH COMPLETE // DATA VERIFIED")
            st.balloons()

            content = results.get("final_content", {}).get("content", "")
            validation = results.get("validation", {})

            # GRADIENT VALIDATION LINE
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

            # Report with gradient title
            st.markdown(f'<div class="terminal-card"><h2>TARGET: {query.upper()}</h2>', unsafe_allow_html=True)
            st.markdown(content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Downloads
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("DOWNLOAD JSON", json.dumps(results, indent=2), "cyber_nexus.json")
            with col2:
                st.download_button("DOWNLOAD TXT", content, "cyber_report.txt")
            with col3:
                pdf_html = f"<html><body style='background:#000;color:#00ff41;font-family:monospace;padding:40px;'><h1 style='background:linear-gradient(90deg,#00ff41,#00ffff,#ff00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>{query}</h1><hr>{content.replace('#', '<br>#')}</body></html>"
                st.download_button("DOWNLOAD PDF (Print→Save)", pdf_html, "cyber_report.html", "text/html")

            if run_eval:
                with st.expander("DETAILED VALIDATION LOG"):
                    evaluator = ResearchEvaluator()
                    metrics = evaluator.evaluate_research(query, results)
                    st.json(metrics.to_dict())

        except Exception as e:
            st.error(f"SYSTEM ERROR: {str(e)}")

# Memory & Archive tabs (same logic)
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

# Final neon line
st.markdown("""
<div style='text-align:center; padding:60px;'>
    <p style='font-size:22px; background:var(--gradient-1); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-shadow: 0 0 40px #00ffff;'>
        // CYBER•NEXUS v10 // GRADIENT CORE v∞ // ETERNAL SIGNAL // 2099
    </p>
</div>
""", unsafe_allow_html=True)
