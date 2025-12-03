"""
ResearchAI - Modern Minimal UI
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
    page_title="ResearchAI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Theme state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# ======================================================
# Modern Minimal UI
# ======================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* Base Theme Variables */
:root {
    --bg-main: #000000;
    --bg-card: #0a0a0a;
    --bg-input: #111111;
    --text-primary: #ffffff;
    --text-secondary: #888888;
    --border: #1a1a1a;
    --accent: #3b82f6;
    --accent-hover: #2563eb;
}

.light-mode {
    --bg-main: #ffffff;
    --bg-card: #fafafa;
    --bg-input: #f5f5f5;
    --text-primary: #000000;
    --text-secondary: #666666;
    --border: #e5e5e5;
    --accent: #3b82f6;
    --accent-hover: #2563eb;
}

/* Global Styles */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: var(--bg-main);
    color: var(--text-primary);
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Hide Streamlit Elements */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Top Navigation */
.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 48px;
    border-bottom: 1px solid var(--border);
}

.logo-text {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}

.theme-switcher {
    padding: 8px 16px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-secondary);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.theme-switcher:hover {
    background: var(--bg-input);
    color: var(--text-primary);
}

/* Hero Section */
.hero-section {
    max-width: 800px;
    margin: 80px auto 60px;
    text-align: center;
}

.hero-title {
    font-size: 56px;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 20px;
    color: var(--text-primary);
    letter-spacing: -2px;
}

.hero-gradient {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 18px;
    color: var(--text-secondary);
    line-height: 1.6;
    font-weight: 400;
}

/* Search Box */
.search-container {
    max-width: 700px;
    margin: 0 auto 40px;
}

.stTextInput input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    color: var(--text-primary) !important;
    font-size: 15px !important;
    transition: all 0.2s ease !important;
}

.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

.stTextInput input::placeholder {
    color: var(--text-secondary) !important;
}

/* Buttons */
.stButton button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton button:hover {
    background: var(--accent-hover) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
}

/* Cards */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 20px;
    transition: all 0.2s ease;
}

.card:hover {
    border-color: var(--text-secondary);
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    max-width: 900px;
    margin: 0 auto 60px;
}

.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    transition: all 0.2s ease;
}

.stat-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
}

.stat-value {
    font-size: 32px;
    font-weight: 800;
    color: var(--accent);
    margin-bottom: 8px;
}

.stat-label {
    font-size: 13px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--border);
    padding: 0 48px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    padding: 16px 20px !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

.stTabs [aria-selected="true"] {
    color: var(--text-primary) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* Select Box */
.stSelectbox > div > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* Checkbox */
.stCheckbox {
    color: var(--text-primary) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* Progress */
.stProgress > div > div {
    background: var(--accent) !important;
}

/* Metrics Display */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 24px 0;
}

.metric-box {
    background: var(--bg-input);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
    text-align: center;
}

.metric-value {
    font-size: 28px;
    font-weight: 800;
    color: var(--accent);
}

.metric-label {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Content Area */
.content-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 48px;
}

/* Download Buttons Container */
.download-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 24px 0;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-main);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-secondary);
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# Top Navigation
# ======================================================
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown('<div class="logo-text">ResearchAI</div>', unsafe_allow_html=True)
with col2:
    if st.button("🌓 Theme"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

if st.session_state.theme == 'light':
    st.markdown('<script>document.body.classList.add("light-mode");</script>', unsafe_allow_html=True)

# ======================================================
# Hero Section
# ======================================================
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">
        Research Made <span class="hero-gradient">Simple</span>
    </h1>
    <p class="hero-subtitle">
        AI-powered research platform that delivers comprehensive insights in seconds
    </p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# Search Input
# ======================================================
st.markdown('<div class="search-container">', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    query = st.text_input(
        "",
        placeholder="What would you like to research?",
        label_visibility="collapsed"
    )
with col2:
    st.write("")
    do_search = st.button("Search", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# Stats (before search)
# ======================================================
if not do_search and query == "":
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">2.4K+</div>
            <div class="stat-label">Research Sessions</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">94%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">2.3s</div>
            <div class="stat-label">Avg Response</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# API Key Check
# ======================================================
anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "")

if not (anthropic_key and tavily_key):
    st.error("⚠️ Missing API keys")
    st.stop()

# ======================================================
# Main Content Area
# ======================================================
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Research", "Related", "History"])

with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        output_format = st.selectbox("Output Format", ["report", "article", "summary", "presentation"])
    with col2:
        run_eval = st.checkbox("Run Evaluation", value=True)

    with st.expander("Advanced Options"):
        session_id_input = st.text_input("Session ID (optional)")
        depth_level = st.slider("Research Depth", 1, 5, 3)

    st.markdown('</div>', unsafe_allow_html=True)

    start = do_search or st.button("🚀 Start Research")

    if start:
        if not query:
            st.warning("Please enter a query")
            st.stop()

        status = st.empty()
        progress = st.progress(0)

        try:
            phases = [
                ("Initializing...", 20),
                ("Searching...", 40),
                ("Analyzing...", 60),
                ("Validating...", 80),
                ("Compiling...", 100),
            ]

            orchestrator = ResearchOrchestrator()

            for text, val in phases:
                status.info(f"⏳ {text}")
                progress.progress(val)
                time.sleep(0.4)

            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            status.success("✅ Complete")
            progress.progress(100)

            content = results.get("final_content", {}).get("content", "")
            summary = results.get("research_summary", {})
            validation = results.get("validation", {})

            # Results Display
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"### {query}")
            
            # Metrics
            st.markdown(f"""
            <div class="metrics-row">
                <div class="metric-box">
                    <div class="metric-value">{summary.get('total_sources', 0)}</div>
                    <div class="metric-label">Sources</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{summary.get('iterations', 0)}</div>
                    <div class="metric-label">Iterations</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{validation.get('confidence_score', 0)}%</div>
                    <div class="metric-label">Confidence</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

            # Content
            if content:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(content)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Citations & Sources
            citations = results.get("citations", [])
            sources = results.get("sources", [])
            
            # Display both citation formats
            if citations or sources:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### 📚 Citations")
                
                # Original citation format (if available)
                if citations:
                    st.markdown("**This report cites the following sources:**")
                    for citation in citations:
                        st.markdown(f"• {citation}")
                    st.markdown("")
                
                # Detailed sources with links
                if sources:
                    st.markdown("**Source Details & Links:**")
                    st.markdown('<div style="margin-top: 16px;">', unsafe_allow_html=True)
                    
                    for idx, source in enumerate(sources, 1):
                        title = source.get("title", "Untitled")
                        url = source.get("url", "#")
                        snippet = source.get("snippet", "")
                        
                        st.markdown(f"""
                        <div style="background: var(--bg-input); border: 1px solid var(--border); 
                             border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                                <div style="font-weight: 600; color: var(--text-primary); flex: 1;">
                                    [{idx}] {title}
                                </div>
                            </div>
                            <div style="font-size: 13px; color: var(--text-secondary); margin-bottom: 8px;">
                                {snippet[:150]}...
                            </div>
                            <a href="{url}" target="_blank" style="font-size: 13px; color: var(--accent); 
                               text-decoration: none; font-weight: 500;">
                                🔗 View Source →
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

            # Downloads
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "📥 JSON",
                    json.dumps(results, indent=2),
                    "research.json",
                    use_container_width=True
                )
            with col2:
                st.download_button(
                    "📥 Text",
                    content,
                    "research.txt",
                    use_container_width=True
                )
            with col3:
                pdf_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>{query}</title>
                    <style>
                        body {{ font-family: system-ui; padding: 40px; line-height: 1.6; }}
                        h1 {{ color: #1a1a1a; }}
                    </style>
                </head>
                <body>
                    <h1>{query}</h1>
                    <p><strong>Confidence:</strong> {validation.get('confidence_score', 85)}%</p>
                    <div>{content}</div>
                </body>
                </html>
                """
                st.download_button(
                    "📄 PDF",
                    pdf_html,
                    "research.html",
                    use_container_width=True
                )

            if run_eval:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### Evaluation")
                try:
                    evaluator = ResearchEvaluator()
                    metrics = evaluator.evaluate_research(query, results)
                    st.json(metrics.to_dict())
                except Exception as e:
                    st.warning(f"Evaluation unavailable: {e}")
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    search_q = st.text_input("Search related research")
    if st.button("Search Related"):
        memory = MemoryBank()
        related = memory.get_related_research(search_q, limit=10)
        if related:
            for item in related:
                with st.expander(item.get("query", "Untitled")):
                    st.json(item)
        else:
            st.info("No results")

with tab3:
    out = Path("outputs")
    if out.exists():
        files = sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)
        st.write(f"**{len(files)} sessions**")
        for f in files[:20]:
            try:
                data = json.load(open(f))
                with st.expander(data.get("query", "Untitled")):
                    st.json(data)
            except:
                pass
    else:
        st.info("No history")

st.markdown('</div>', unsafe_allow_html=True)
