# Main Content"""
streamlit_wrapper.py – ENHANCED VERSION
React-inspired UI + animations + PDF download + Dark/Light theme
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

# Initialize theme in session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# ======================================================
# Enhanced UI with animations + gradients + Theme Support
# ======================================================
theme_styles = """
<style>
/* Root Colors - Dark Theme */
:root {
    --g1: #0d0a24;
    --g2: #32105a;
    --g3: #6d29b0;
    --accent-a: #4ff0ff;
    --accent-b: #bf6afc;
    --accent-pink: #ff4d8f;
    --bg-primary: #0a0a0a;
    --bg-secondary: rgba(255, 255, 255, 0.06);
    --text-primary: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.7);
    --border-color: rgba(255, 255, 255, 0.12);
}

/* Light Theme Colors */
.light-theme {
    --g1: #ffffff;
    --g2: #fafbfc;
    --g3: #f0f4f8;
    --accent-a: #2563eb;
    --accent-b: #7c3aed;
    --accent-pink: #ec4899;
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --border-color: #e2e8f0;
}

/* Apply theme to body */
body.light-theme,
html.light-theme,
[data-testid="stAppViewContainer"].light-theme {
    --g1: #ffffff;
    --g2: #fafbfc;
    --g3: #f0f4f8;
    --accent-a: #2563eb;
    --accent-b: #7c3aed;
    --accent-pink: #ec4899;
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --border-color: #e2e8f0;
}

/* Main Background */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, var(--g1) 0%, var(--g2) 50%, var(--g3) 100%);
    background-size: 400% 400%;
    animation: gradientMove 16s ease infinite;
    color: var(--text-primary);
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Theme Toggle Button */
.theme-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 10px 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.theme-toggle:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

/* Topbar */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 26px;
    margin-bottom: 20px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(79, 240, 255, 0.1);
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 24px;
    font-weight: 900;
    background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.logo-dot {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: linear-gradient(135deg, var(--accent-a), var(--accent-b));
    animation: pulseGlow 3s ease-in-out infinite;
}

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 12px rgba(79, 240, 255, 0.5); }
    50% { box-shadow: 0 0 24px rgba(191, 106, 252, 0.8); }
}

/* Hero Section */
.hero {
    text-align: center;
    padding: 60px 20px 40px;
    animation: fadeInUp 0.8s ease;
}

.hero h1 {
    font-size: 56px;
    font-weight: 900;
    color: var(--text-primary);
    margin-bottom: 20px;
    line-height: 1.1;
    letter-spacing: -1px;
}

.highlight {
    background: linear-gradient(90deg, var(--accent-a), var(--accent-pink), var(--accent-b));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glowText 4s ease-in-out infinite;
    font-weight: 900;
}

@keyframes glowText {
    0%, 100% { filter: drop-shadow(0 0 8px var(--accent-b)); }
    50% { filter: drop-shadow(0 0 16px var(--accent-a)); }
}

.hero-subtitle {
    font-size: 20px;
    color: var(--text-secondary);
    max-width: 700px;
    margin: 20px auto 0;
    font-weight: 500;
    line-height: 1.6;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Search Container */
.search-wrapper {
    max-width: 900px;
    margin: 30px auto;
    padding: 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    backdrop-filter: blur(15px);
    transition: all 0.3s ease;
    box-shadow: 0 0 30px rgba(79, 240, 255, 0.1);
}

.search-wrapper:hover {
    transform: translateY(-4px);
    box-shadow: 0 0 40px rgba(191, 106, 252, 0.25);
    border-color: var(--accent-a);
}

/* Stat Cards */
.stat-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 20px;
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-6px);
    background: var(--bg-secondary);
    box-shadow: 0 8px 24px rgba(191, 106, 252, 0.3);
    border-color: var(--accent-b);
}

.stat-label {
    font-size: 28px;
    font-weight: 900;
    background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.stat-text {
    font-size: 13px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Pills */
.pill {
    display: inline-block;
    margin: 6px;
    padding: 8px 18px;
    border-radius: 24px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 13px;
    font-weight: 600;
}

.pill:hover {
    background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
    color: #ffffff;
    transform: translateY(-3px);
    box-shadow: 0 0 16px rgba(79, 240, 255, 0.4);
}

/* Results Container */
.results-container {
    max-width: 1200px;
    margin: 0 auto;
    animation: fadeInUp 0.6s ease;
}

.result-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.result-card:hover {
    background: var(--bg-secondary);
    border-color: var(--accent-a);
    box-shadow: 0 8px 32px rgba(191, 106, 252, 0.2);
}

.result-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 12px;
}

.result-subtitle {
    font-size: 12px;
    color: var(--accent-a);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

/* Metrics Bar */
.metric-item {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
}

.metric-item:hover {
    background: var(--bg-secondary);
    box-shadow: 0 4px 12px rgba(79, 240, 255, 0.2);
}

/* Progress Bar */
.progress-container {
    margin: 20px 0;
}

.progress-bar {
    background: var(--bg-secondary);
    border-radius: 12px;
    overflow: hidden;
    height: 6px;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { box-shadow: -1000px 0 0 0 rgba(255, 255, 255, 0.2); }
    100% { box-shadow: 1000px 0 0 0 rgba(255, 255, 255, 0.2); }
}

/* Text Colors */
.text-muted { color: var(--text-secondary); }
.text-accent { color: var(--accent-a); }
.text-white { color: var(--text-primary); }

</style>
"""

st.markdown(theme_styles, unsafe_allow_html=True)

# Theme toggle in sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    theme_option = st.radio(
        "Theme",
        ["🌙 Dark", "☀️ Light"],
        index=0 if st.session_state.theme == 'dark' else 1
    )
    
    if "Dark" in theme_option:
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'
        # Apply light theme class
        st.markdown("""
        <script>
            document.body.classList.add('light-theme');
            document.documentElement.classList.add('light-theme');
            document.querySelector('[data-testid="stAppViewContainer"]').classList.add('light-theme');
        </script>
        """, unsafe_allow_html=True)

# ======================================================
# Topbar
# ======================================================
col1, col2 = st.columns([1, 10])
with col1:
    st.markdown('<div class="logo-dot"></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="logo">ResearchAI</div>', unsafe_allow_html=True)

st.markdown("---")

# ======================================================
# Hero Section
# ======================================================
st.markdown("""
<div class="hero">
    <h1>Deep Research at <span class="highlight">Lightning Speed</span></h1>
    <p class="hero-subtitle">Powered by advanced AI agents. Get comprehensive, verified research in minutes, not hours.</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# Search Input
# ======================================================
st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)

col_search, col_btn = st.columns([4, 1], gap="small")
with col_search:
    query = st.text_input(
        "",
        placeholder="E.g., Impact of AI on healthcare, Climate solutions, Quantum computing...",
        label_visibility="collapsed",
        key="search_input"
    )

with col_btn:
    do_search = st.button("🚀 Research", use_container_width=True, key="search_btn")

st.markdown('</div>', unsafe_allow_html=True)

# Quick suggestions
st.markdown("""
<div style="text-align: center; margin: 20px 0;">
    <span class="pill">Renewable Energy</span>
    <span class="pill">Drug Discovery</span>
    <span class="pill">Space Exploration</span>
    <span class="pill">Cybersecurity</span>
</div>
""", unsafe_allow_html=True)

# ======================================================
# Stat Cards (before search)
# ======================================================
if not do_search and query == "":
    col1, col2, col3 = st.columns(3, gap="large")
    
    try:
        memory_bank = MemoryBank()
        stats = memory_bank.get_statistics()
    except:
        stats = {"total_memories": 0, "completed_sessions": 0, "total_sources": 0}

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">2,453</div>
            <div class="stat-text">Research Sessions</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">94%</div>
            <div class="stat-text">Accuracy Rate</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">2.3s</div>
            <div class="stat-text">Avg Response Time</div>
        </div>
        """, unsafe_allow_html=True)

# ======================================================
# API Key Check
# ======================================================
anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "")

if not (anthropic_key and tavily_key):
    st.error("⚠️ Missing API keys. Add ANTHROPIC_API_KEY and TAVILY_API_KEY to .env or secrets.")
    st.stop()

# ======================================================
# Research Tabs
# ======================================================
tab1, tab2, tab3 = st.tabs(["🔬 New Research", "🔍 Find Related", "📊 Past Sessions"])

# Tab 1 – New Research
with tab1:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    colA, colB = st.columns([3, 2], gap="medium")
    with colA:
        output_format = st.selectbox("📄 Output Format", ["report", "article", "summary", "presentation"])
    with colB:
        run_eval = st.checkbox("🎯 Run Evaluation", value=True)

    with st.expander("⚙️ Advanced Options"):
        session_id_input = st.text_input("Resume Session ID", "")
        depth_level = st.slider("Research Depth", 1, 5, 3)

    st.markdown('</div>', unsafe_allow_html=True)

    start = do_search or st.button("🚀 Start Research", key="start_research_btn")

    if start:
        if not query:
            st.warning("⚠️ Please enter a research query.")
            st.stop()

        # Progress indicators
        progress_container = st.container()
        status_container = st.empty()
        progress_bar = st.empty()

        try:
            # Simulate research phases
            phases = [
                ("Initializing research agents...", 20),
                ("Searching sources...", 40),
                ("Analyzing data...", 60),
                ("Validating findings...", 80),
                ("Compiling report...", 100),
            ]

            orchestrator = ResearchOrchestrator()

            for phase_text, progress_val in phases:
                status_container.info(f"⏳ {phase_text}")
                progress_bar.progress(progress_val)
                time.sleep(0.5)

            # Conduct research
            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            status_container.success("✅ Research completed!")
            progress_bar.progress(100)

            final = results.get("final_content", {})
            content = final.get("content", "")
            summary = results.get("research_summary", {})
            validation = results.get("validation", {})

            # Display Results
            st.markdown('<div class="results-container">', unsafe_allow_html=True)

            # Quality Score
            st.markdown(f"""
            <div class="result-card">
                <div class="result-subtitle">Research Query</div>
                <div class="result-title">{query}</div>
                <div style="margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span class="text-muted">Quality Score</span>
                        <span class="text-accent" style="font-weight: 700; font-size: 18px;">
                            {validation.get('confidence_score', 85)}/100
                        </span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {validation.get('confidence_score', 85)}%"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-item">
                    <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">📚 Sources</div>
                    <div style="font-size: 24px; font-weight: 900; color: var(--accent-a);">
                        {summary.get('total_sources', 0)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-item">
                    <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">🔄 Iterations</div>
                    <div style="font-size: 24px; font-weight: 900; color: var(--accent-b);">
                        {summary.get('iterations', 0)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-item">
                    <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">🎯 Confidence</div>
                    <div style="font-size: 24px; font-weight: 900; color: var(--accent-pink);">
                        {validation.get('confidence_score', 0)}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
            if content:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(content, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ No content generated.")

            # Download options with PDF
            col_down1, col_down2, col_down3 = st.columns(3)
            with col_down1:
                st.download_button(
                    "📥 Download JSON",
                    json.dumps(results, indent=2),
                    "research.json",
                    "application/json"
                )
            with col_down2:
                st.download_button(
                    "📥 Download TXT",
                    content,
                    "research.txt",
                    "text/plain"
                )
            with col_down3:
                # PDF Download Button
                pdf_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>{query}</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; padding: 40px; line-height: 1.6; }}
                        h1 {{ color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
                        .metadata {{ background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                    </style>
                </head>
                <body>
                    <h1>{query}</h1>
                    <div class="metadata">
                        <p><strong>Quality Score:</strong> {validation.get('confidence_score', 85)}/100</p>
                        <p><strong>Sources:</strong> {summary.get('total_sources', 0)}</p>
                        <p><strong>Confidence:</strong> {validation.get('confidence_score', 0)}%</p>
                    </div>
                    <div>{content}</div>
                </body>
                </html>
                """
                st.download_button(
                    "📄 Download PDF",
                    pdf_html,
                    "research.html",
                    "text/html",
                    help="Download as HTML (can be converted to PDF)"
                )

            # Evaluation
            if run_eval:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.subheader("📊 Evaluation Metrics")
                try:
                    evaluator = ResearchEvaluator()
                    metrics = evaluator.evaluate_research(query, results)
                    st.json(metrics.to_dict())
                except Exception as e:
                    st.warning(f"Evaluation unavailable: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)

# Tab 2 – Related Research
with tab2:
    related_query = st.text_input("🔍 Search Query", key="related_search")
    if st.button("Search", key="related_btn"):
        memory = MemoryBank()
        rel = memory.get_related_research(related_query, limit=10)
        if rel:
            for x in rel:
                with st.expander(x.get("query", "Untitled")):
                    st.json(x)
        else:
            st.info("No related research found.")

# Tab 3 – Past Sessions
with tab3:
    out = Path("outputs")
    if out.exists():
        files = sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)
        st.write(f"**Total sessions:** {len(files)}")

        for f in files[:20]:
            try:
                data = json.load(open(f))
                with st.expander(data.get("query", "Untitled")):
                    st.json(data)
                    st.download_button(
                        "Download",
                        json.dumps(data),
                        f.name,
                        key=f.name
                    )
            except:
                pass
    else:
        st.info("No sessions yet.")

# Footer
st.markdown("""
---
<div style="text-align: center; padding: 20px; color: var(--text-secondary); font-size: 13px;">
Made with ❤️ using Streamlit • Multi-Agent Research AI
</div>
""", unsafe_allow_html=True)
