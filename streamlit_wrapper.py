"""
streamlit_wrapper.py — FINAL FULL VERSION
UI upgraded with animations + glow + gradients 
Logic 100% unchanged.
"""

import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

# --- Core Logic (unchanged) ---
from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator
from memory.memory_bank import MemoryBank

# ======================================================
# Page config
# ======================================================
st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# UI — Enhanced Animations + Colors
# ======================================================
st.markdown("""
<style>
/* ------------------------------ */
/*  🔥 Animated Background         */
/* ------------------------------ */
:root {
    --g1: #0d0a24;
    --g2: #32105a;
    --g3: #6d29b0;
    --accent-a: #4ff0ff;
    --accent-b: #bf6afc;
}

html, body, .block-container {
    background: linear-gradient(135deg, var(--g1), var(--g2), var(--g3));
    background-size: 400% 400%;
    animation: gradientMove 16s ease infinite;
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ------------------------------ */
/*  🔥 Topbar                     */
/* ------------------------------ */
.topbar {
    display: flex;
    justify-content: space-between;
    padding: 16px 26px;
    margin-bottom: 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    backdrop-filter: blur(10px);
    transition: .3s ease;
}
.topbar:hover {
    box-shadow: 0 0 18px rgba(158, 99, 255, 0.35);
}

/* Logo + Animated dot */
.logo {
    color: white;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 9px;
}
.logo .dot {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
    animation: pulseGlow 3s ease-in-out infinite;
}
@keyframes pulseGlow {
    0% { box-shadow: 0 0 4px #984dff; }
    50% { box-shadow: 0 0 16px #4ff0ff; }
    100% { box-shadow: 0 0 4px #984dff; }
}

/* ------------------------------ */
/*  🔥 Hero                       */
/* ------------------------------ */
.hero {
    text-align: center;
    padding: 40px 10px 20px;
}

.hero h1 {
    font-size: 38px;
    font-weight: 900;
    color: white;
    animation: fadeSlide 1.2s ease;
}

@keyframes fadeSlide {
    0% { opacity: 0; transform: translateY(22px); }
    100% { opacity: 1; transform: translateY(0); }
}

.highlight {
    background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glowText 4s ease-in-out infinite;
}

@keyframes glowText {
    0% { filter: drop-shadow(0 0 4px var(--accent-b)); }
    50% { filter: drop-shadow(0 0 10px var(--accent-a)); }
    100% { filter: drop-shadow(0 0 4px var(--accent-b)); }
}

.hero p.sub {
    color: rgba(240,240,255,0.85);
    margin-top: 8px;
}

/* ------------------------------ */
/*  🔥 Search Bar                 */
/* ------------------------------ */
.search-container {
    max-width: 820px;
    margin: 20px auto;
    padding: 14px;
    display: flex;
    gap: 12px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    backdrop-filter: blur(12px);
    transition: .3s ease;
}
.search-container:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 20px rgba(158, 99, 255, 0.35);
}

/* Input override */
.search-container .stTextInput > div > div > input {
    background: transparent !important;
    border: none !important;
    color: white !important;
    font-size: 15px;
}

/* Search button */
.search-btn > button {
    background: linear-gradient(90deg, #4ac9ff, #994bff) !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    transition: .2s;
}
.search-btn > button:hover {
    transform: scale(1.06);
    box-shadow: 0 0 14px rgba(155, 88, 255, 0.45);
}

/* ------------------------------ */
/*  🔥 Pills                      */
/* ------------------------------ */
.pill {
    display: inline-block;
    margin: 6px;
    padding: 6px 16px;
    border-radius: 20px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    color: #e9f0ff;
    transition: .25s;
    cursor: pointer;
}
.pill:hover {
    background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
    color: #1d1333;
    transform: translateY(-3px);
    box-shadow: 0 0 10px rgba(140, 75, 255, 0.45);
}

/* ------------------------------ */
/*  🔥 Metric Card Hover          */
/* ------------------------------ */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 14px;
    border-radius: 14px;
    transition: .3s;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 16px rgba(155, 88, 255, 0.35);
}

</style>
""", unsafe_allow_html=True)

# ======================================================
#  Topbar
# ======================================================
st.markdown("""
<div class="topbar">
    <div class="logo">
        <div class="dot"></div> ResearchAI
    </div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# Hero Section
# ======================================================
st.markdown("""
<div class="hero">
    <h1>Deep Research at <span class="highlight">Lightning Speed</span></h1>
    <p class="sub">Powered by advanced AI agents. Get comprehensive, verified research in minutes, not hours.</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# Search UI
# ======================================================
st.markdown("<div class='search-container'>", unsafe_allow_html=True)

col_left, col_right = st.columns([8, 2], gap="small")

with col_left:
    query = st.text_input(
        "",
        placeholder="E.g., Impact of AI on healthcare, Climate solutions, Quantum computing...",
        label_visibility="collapsed"
    )

with col_right:
    do_search = st.button("Research", key="ui_search_btn", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;">
    <span class="pill">Renewable Energy</span>
    <span class="pill">Drug Discovery</span>
    <span class="pill">Space Exploration</span>
    <span class="pill">Cybersecurity</span>
</div>
""", unsafe_allow_html=True)

st.session_state["ui_search_trigger"] = do_search

# ======================================================
# Sidebar Stats
# ======================================================
with st.sidebar:
    st.markdown("### 📊 Research Analytics")
    try:
        memory_bank = MemoryBank()
        stats = memory_bank.get_statistics()
        st.metric("Total Research", stats.get("total_memories", 0))
        st.metric("Completed", stats.get("completed_sessions", 0))
        st.metric("Sources", stats.get("total_sources", 0))
        st.metric("Avg Quality", f"{stats.get('avg_importance', 0):.1f}/10")
    except:
        st.info("Stats unavailable")

    st.markdown("---")
    st.markdown("### Recent Activity")
    out = Path("outputs")
    if out.exists():
        files = sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)[:6]
        for f in files:
            try:
                d = json.load(open(f))
                st.write("• " + d.get("query", "")[:45] + "...")
            except:
                pass

# ======================================================
# API Key check
# ======================================================
anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "")

if not (anthropic_key and tavily_key):
    st.error("Missing API keys.")
    st.stop()

# ======================================================
# Tabs
# ======================================================
tab1, tab2, tab3 = st.tabs(["🔬 New Research", "🔍 Find Related", "📂 Past Sessions"])

# ------------------------------------------------------
# Tab 1 — New Research
# ------------------------------------------------------
with tab1:
    st.markdown("## 🔬 New Research")

    colA, colB = st.columns([3, 2])
    with colA:
        output_format = st.selectbox("📄 Output Format", ["report", "article", "summary", "presentation"])
    with colB:
        run_eval = st.checkbox("🎯 Run Evaluation", value=True)

    with st.expander("⚙️ Advanced Options"):
        session_id_input = st.text_input("Resume Session ID", "")
        depth_level = st.slider("Research Depth", 1, 5, 3)

    start = st.session_state.get("ui_search_trigger", False) or st.button("🚀 Start Research")

    if start:
        if not query:
            st.warning("Enter a research query.")
            st.stop()

        progress = st.progress(0)
        status = st.empty()

        try:
            status.info("Initializing agents...")
            progress.progress(20)

            orchestrator = ResearchOrchestrator()
            status.info("Researching...")
            progress.progress(60)

            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            progress.progress(100)
            st.success("Research completed!")
            status.empty()

            final = results.get("final_content", {})
            content = final.get("content", "")
            summary = results.get("research_summary", {})
            validation = results.get("validation", {})

            st.metric("📚 Sources", summary.get("total_sources", 0))
            st.metric("🔄 Iterations", summary.get("iterations", 0))
            st.metric("🎯 Confidence", f"{validation.get('confidence_score', 0)}%")

            if not content:
                st.warning("No output generated.")
            else:
                st.markdown(content, unsafe_allow_html=True)

            st.download_button("📥 Download JSON", json.dumps(results, indent=2), "research.json")
            st.download_button("📥 Download TXT", content, "research.txt")

            if run_eval:
                evaluator = ResearchEvaluator()
                metrics = evaluator.evaluate_research(query, results)
                st.write(metrics.to_dict())

        except Exception as e:
            st.error(str(e))
            st.exception(e)

# ------------------------------------------------------
# Tab 2 — Related Research
# ------------------------------------------------------
with tab2:
    related_query = st.text_input("Search Query")

    if st.button("🔎 Search"):
        memory = MemoryBank()
        rel = memory.get_related_research(related_query, limit=10)
        if rel:
            for x in rel:
                with st.expander(x.get("query", "Untitled")):
                    st.write(x)
        else:
            st.info("No related research found.")

# ------------------------------------------------------
# Tab 3 — Past Sessions
# ------------------------------------------------------
with tab3:
    out = Path("outputs")
    if out.exists():
        files = sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)
        st.write(f"Total sessions: {len(files)}")

        for f in files[:20]:
            data = json.load(open(f))
            with st.expander(data.get("query", "Untitled")):
                st.json(data)
                st.download_button("Download", json.dumps(data), f.name)
    else:
        st.info("No sessions yet.")

# Footer
st.markdown("""
<div style="text-align:center; padding:20px; color:#ddd;">
Made with ❤️ using Streamlit • Multi Agent Research AI
</div>
""", unsafe_allow_html=True)
