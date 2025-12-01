"""
Streamlit Web Interface for AI Research Assistant
With Screenshot UI Styling (ResearchAI Theme)
"""
import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator
from memory.memory_bank import MemoryBank

# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Screenshot UI CSS
# ---------------------------
st.markdown("""
<style>

:root {
    --purple-light: #c084fc;
    --purple: #a855f7;
    --blue: #3b82f6;
    --cyan: #22d3ee;
    --bg-dark: #080b1b;
    --glass: rgba(255,255,255,0.05);
    --border-glow: rgba(255,255,255,0.15);
}

body {
    background: #080b1b !important;
}

.main {
    background: #080b1b;
}

.hero {
    margin-top: 10px;
    padding: 60px 20px;
    text-align: center;
    background: radial-gradient(circle at top right, #3b0fff40, #000000),
                linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    border-radius: 20px;
    border: 1px solid var(--border-glow);
    box-shadow: 0 0 40px #0004 inset;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    color: white;
}

.hero-title span {
    background: linear-gradient(90deg, #22d3ee, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    margin-top: 10px;
    font-size: 1.1rem;
    color: #cbd5e1;
}

.search-box {
    margin: 30px auto;
    padding: 25px;
    max-width: 900px;
    background: var(--glass);
    border-radius: 16px;
    border: 1px solid var(--border-glow);
    backdrop-filter: blur(10px);
}

.tag-btn {
    display: inline-block;
    padding: 6px 14px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 30px;
    color: #e2e8f0;
    font-size: 0.8rem;
    margin-right: 8px;
    transition: 0.2s;
}

.tag-btn:hover {
    background: rgba(255,255,255,0.18);
    transform: translateY(-2px);
}

.stat-container {
    margin-top: 40px;
    display: flex;
    gap: 20px;
    justify-content: center;
}

.stat-card {
    flex: 1;
    padding: 30px;
    background: var(--glass);
    border-radius: 20px;
    border: 1px solid var(--border-glow);
    min-width: 260px;
}

.stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: white;
}

.stat-label {
    font-size: 0.9rem;
    color: #cbd5e1;
    margin-top: -5px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# HERO SECTION
# --------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">
        Deep Research at <span>Lightning Speed</span>
    </div>
    <div class="hero-sub">
        Powered by advanced AI agents. Get comprehensive, verified research in minutes, not hours.
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------
# SEARCH UI
# --------------------------

st.markdown("<div class='search-box'>", unsafe_allow_html=True)

query = st.text_input(
    "",
    placeholder="E.g., Impact of AI on healthcare, Climate solutions, Quantum computing...",
    key="main_query_box"
)

cols = st.columns([1, 5])
with cols[0]:
    click_research = st.button("Research", use_container_width=True)

st.markdown("""
<br>
<span class="tag-btn">Renewable Energy</span>
<span class="tag-btn">Drug Discovery</span>
<span class="tag-btn">Space Exploration</span>
<span class="tag-btn">Cybersecurity</span>
</div>
""", unsafe_allow_html=True)

# --------------------------
# STATIC METRIC CARDS (as shown in screenshot)
# --------------------------
st.markdown("""
<div class="stat-container">
    <div class="stat-card">
        <div class="stat-number">2,453</div>
        <div class="stat-label">Research Sessions</div>
    </div>

    <div class="stat-card">
        <div class="stat-number">94%</div>
        <div class="stat-label">Accuracy Rate</div>
    </div>

    <div class="stat-card">
        <div class="stat-number">2.3s</div>
        <div class="stat-label">Avg Response Time</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------
# Sidebar
# ------------------------

with st.sidebar:
    st.header("📊 Research Analytics")

    try:
        memory_bank = MemoryBank()
        stats = memory_bank.get_statistics()

        st.metric("Total Research", stats.get("total_memories", 0))
        st.metric("Completed Sessions", stats.get("completed_sessions", 0))
        st.metric("Total Sources", stats.get("total_sources", 0))
        st.metric("Avg Quality", f"{stats.get('avg_importance', 0):.1f}/10")
    except:
        st.info("Stats available after first research.")

    st.markdown("---")
    st.subheader("Recent Activity")

    output_dir = Path("outputs")
    if output_dir.exists():
        json_files = list(output_dir.glob("*.json"))
        for file in sorted(json_files, key=os.path.getmtime, reverse=True)[:6]:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    title = data.get("query", "Untitled")
                    st.write("• " + title[:40] + "...")
            except:
                pass

# API Keys
anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "")

if anthropic_key:
    os.environ["ANTHROPIC_API_KEY"] = anthropic_key
if tavily_key:
    os.environ["TAVILY_API_KEY"] = tavily_key

if not (anthropic_key and tavily_key):
    st.error("⚠️ API Keys missing. Add ANTHROPIC_API_KEY and TAVILY_API_KEY to .env")
    st.stop()

# ------------------------------
# MAIN LOGIC BELOW (UNCHANGED)
# ------------------------------

# Tabs
tab1, tab2, tab3 = st.tabs(["🔬 New Research", "🔍 Find Related", "📂 Past Sessions"])

# ---------------- TAB 1 ----------------
with tab1:
    st.subheader("Start New Research")

    col1, col2 = st.columns([3, 2])
    output_format = col1.selectbox("Output Format", ["report", "article", "summary", "presentation"])
    run_evaluation = col2.checkbox("Run Evaluation", value=True)

    with st.expander("Advanced Options"):
        session_id_input = st.text_input("Resume Session ID", placeholder="research_xxxxx")
        depth_level = st.slider("Research Depth", 1, 5, 3)

    if click_research or st.button("🚀 Start Research"):
        if not query:
            st.warning("Please enter a research query.")
            st.stop()

        progress = st.progress(10)
        status = st.empty()

        try:
            status.info("Initializing research...")
            progress.progress(30)
            orchestrator = ResearchOrchestrator()

            status.info("Processing…")
            progress.progress(60)

            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )

            progress.progress(100)
            status.info("Research completed!")

            final_content = results.get("final_content", {})
            summary = results.get("research_summary", {})
            validation = results.get("validation", {})

            st.success("Research completed successfully!")

            # Metrics
            colA, colB, colC, colD = st.columns(4)
            colA.metric("Sources", summary.get("total_sources", 0))
            colB.metric("Iterations", summary.get("iterations", 0))
            colC.metric("Confidence", f"{validation.get('confidence_score', 0)}%")
            colD.metric("Format", output_format.title())

            # Output
            st.markdown("## Generated Content")
            content = final_content.get("content", "")
            st.markdown(content)

            # Downloads
            st.download_button("Download Markdown", content, "research.md")
            st.download_button("Download JSON", json.dumps(results, indent=2), "research.json")
            st.download_button("Download TXT", content, "research.txt")

            # Evaluation
            if run_evaluation:
                st.markdown("## Quality Evaluation")
                eval_engine = ResearchEvaluator()
                metrics = eval_engine.evaluate_research(query, results)
                scores = metrics.to_dict()

                for k, v in scores.items():
                    st.metric(k.title(), f"{v}/100")

                st.subheader(f"Overall Score: {metrics.overall_score}/100")

        except Exception as e:
            st.error(f"Research failed: {str(e)}")
            st.exception(e)

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("Find Related Research")

    related_query = st.text_input("Search related research")

    if st.button("Search Related"):
        memory_bank = MemoryBank()
        related = memory_bank.get_related_research(related_query, limit=10)

        if not related:
            st.info("No related research found.")
        else:
            for item in related:
                with st.expander(item.get("query", "Untitled")):
                    st.write(item)

# ---------------- TAB 3 ----------------
with tab3:
    st.subheader("Past Research Sessions")

    output_dir = Path("outputs")
    if output_dir.exists():
        files = list(output_dir.glob("*.json"))

        for file in sorted(files, key=os.path.getmtime, reverse=True):
            with open(file, "r") as f:
                data = json.load(f)

            with st.expander(data.get("query", "Untitled")):
                st.json(data)
                st.download_button("Download", json.dumps(data, indent=2), file.name)

# Footer
st.markdown("""
<br><br>
<center style='color:#777;'>AI Research Assistant v2.0 • Built with ❤️ using Streamlit</center>
""", unsafe_allow_html=True)
