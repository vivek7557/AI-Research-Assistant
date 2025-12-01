"""
Streamlit Web Interface for AI Research Assistant
Clean Version + Screenshot UI
"""

import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

# Your actual logic (unchanged)
from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator
from memory.memory_bank import MemoryBank


# ======================================================
#  PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)


# ======================================================
#  GLOBAL UI CSS
# ======================================================
st.markdown("""
<style>

:root {
    --purple-light: #c084fc;
    --purple: #a855f7;
    --blue: #3b82f6;
    --cyan: #22d3ee;
    --bg-dark: #0a0f1f;
    --glass: rgba(255,255,255,0.06);
    --border-glow: rgba(255,255,255,0.12);
}

html, body, .block-container {
    background: var(--bg-dark) !important;
}

/* HERO SECTION */
.hero {
    margin-top: 18px;
    padding: 75px 25px;
    text-align: center;
    background: linear-gradient(135deg, #151336, #1e1752, #0c0f28);
    border-radius: 24px;
    border: 1px solid var(--border-glow);
    box-shadow: 0 0 50px #0007 inset;
}

.hero-title {
    font-size: 3.3rem;
    font-weight: 900;
    color: white;
}

.hero-title span {
    background: linear-gradient(90deg, #22d3ee, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    margin-top: 12px;
    font-size: 1.2rem;
    color: #cbd5e1;
}

/* SEARCH BOX */
.search-box {
    margin: 32px auto;
    padding: 28px;
    max-width: 900px;
    background: var(--glass);
    border-radius: 18px;
    border: 1px solid var(--border-glow);
    backdrop-filter: blur(12px);
}

/* TAGS */
.tag-btn {
    display: inline-block;
    padding: 6px 14px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 30px;
    color: #e2e8f0;
    font-size: 0.82rem;
    margin-right: 8px;
    transition: 0.25s;
}
.tag-btn:hover {
    background: rgba(255,255,255,0.18);
    transform: translateY(-2px);
}

/* METRICS */
.stats-container {
    margin-top: 40px;
    display: flex;
    gap: 22px;
    justify-content: center;
}

.stat-card {
    flex: 1;
    padding: 32px;
    background: var(--glass);
    border-radius: 20px;
    border: 1px solid var(--border-glow);
    min-width: 260px;
    text-align: center;
}

.stat-number {
    font-size: 2.3rem;
    font-weight: 800;
    color: white;
}

.stat-label {
    font-size: 1rem;
    color: #cbd5e1;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
#  HERO UI
# ======================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">
        Deep Research at <span>Lightning Speed</span>
    </div>
    <div class="hero-sub">
        Powered by advanced AI agents. Get comprehensive, verified research in minutes — not hours.
    </div>
</div>
""", unsafe_allow_html=True)


# ======================================================
#  SEARCH BAR UI
# ======================================================
st.markdown("<div class='search-box'>", unsafe_allow_html=True)

query = st.text_input(
    "",
    placeholder="E.g., Impact of AI in healthcare, Quantum computing, Climate solutions..."
)

cols = st.columns([1, 5])
with cols[0]:
    hero_search_clicked = st.button("Research", use_container_width=True)

st.markdown("""
<br>
<span class="tag-btn">Renewable Energy</span>
<span class="tag-btn">Drug Discovery</span>
<span class="tag-btn">Space Exploration</span>
<span class="tag-btn">Cybersecurity</span>
</div>
""", unsafe_allow_html=True)


# ======================================================
#  STATIC METRIC CARDS (from screenshot)
# ======================================================
st.markdown("""
<div class="stats-container">
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


# ======================================================
#  SIDEBAR (clean and simple)
# ======================================================

with st.sidebar:
    st.title("📊 Research Analytics")

    try:
        mb = MemoryBank()
        stats = mb.get_statistics()

        st.metric("Total Research", stats.get("total_memories", 0))
        st.metric("Completed Sessions", stats.get("completed_sessions", 0))
        st.metric("Total Sources", stats.get("total_sources", 0))
        st.metric("Avg Quality", f"{stats.get('avg_importance', 0):.1f}/10")

    except:
        st.info("Stats will appear after first research.")

    st.write("---")
    st.subheader("Recent Activity")

    out_dir = Path("outputs")
    if out_dir.exists():
        files = list(out_dir.glob("*.json"))
        for f in sorted(files, key=os.path.getmtime, reverse=True)[:6]:
            try:
                data = json.load(open(f))
                st.write("•", data.get("query", "Untitled")[:40] + "…")
            except:
                pass


# ======================================================
#  CHECK API KEYS
# ======================================================

anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY", "")

if not anthropic_key or not tavily_key:
    st.error("Missing API Keys in .env")
    st.stop()


# ======================================================
#  TABS
# ======================================================
tab1, tab2, tab3 = st.tabs(["🔬 New Research", "🔍 Find Related", "📂 Past Sessions"])


# ======================================================
#  TAB 1 — NEW RESEARCH
# ======================================================
with tab1:

    st.subheader("Start New Research")

    colA, colB = st.columns([3, 2])
    out_format = colA.selectbox("Output Format", ["report", "article", "summary", "presentation"])
    eval_on = colB.checkbox("Run Evaluation", value=True)

    with st.expander("Advanced"):
        session_id = st.text_input("Resume Session ID")
        depth = st.slider("Research Depth", 1, 5, 3)

    # Start research button
    start_clicked = hero_search_clicked or st.button("🚀 Start Research")

    if start_clicked:
        if not query:
            st.warning("Enter a research query first.")
            st.stop()

        st.info("⏳ Processing...")
        prog = st.progress(10)

        try:
            prog.progress(35)
            orch = ResearchOrchestrator()

            prog.progress(55)
            results = orch.conduct_research(
                query=query,
                output_format=out_format,
                session_id=session_id or None
            )

            prog.progress(100)
            st.success("✅ Research complete!")

            final = results.get("final_content", {})
            summary = results.get("research_summary", {})
            validation = results.get("validation", {})

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Sources", summary.get("total_sources", 0))
            c2.metric("Iterations", summary.get("iterations", 0))
            c3.metric("Confidence", f"{validation.get('confidence_score', 0)}%")
            c4.metric("Format", out_format)

            st.write("---")
            st.subheader("📄 Generated Research")
            st.markdown(final.get("content", ""))

            st.download_button("Download .md", final.get("content",""), "research.md")
            st.download_button("Download .json", json.dumps(results, indent=2), "research.json")
            st.download_button("Download .txt", final.get("content",""), "research.txt")

            if eval_on:
                st.write("---")
                st.subheader("📊 Evaluation")

                evaluator = ResearchEvaluator()
                metrics = evaluator.evaluate_research(query, results)

                for k, v in metrics.to_dict().items():
                    st.metric(k.title(), f"{v}/100")

                st.success(f"Overall Score: {metrics.overall_score}/100")

        except Exception as e:
            st.error("❌ Research failed")
            st.exception(e)


# ======================================================
#  TAB 2 — RELATED
# ======================================================
with tab2:
    st.subheader("Find Related Research")
    rq = st.text_input("Search related queries")

    if st.button("Search"):
        mb = MemoryBank()
        related = mb.get_related_research(rq, limit=12)

        if not related:
            st.info("No related research found.")
        else:
            for r in related:
                with st.expander(r.get("query", "Untitled")):
                    st.json(r)


# ======================================================
#  TAB 3 — HISTORY
# ======================================================
with tab3:
    st.subheader("Past Sessions")

    out_dir = Path("outputs")

    if out_dir.exists():
        files = list(out_dir.glob("*.json"))
        for f in sorted(files, key=os.path.getmtime, reverse=True):
            data = json.load(open(f))
            with st.expander(data.get("query", "Untitled")):
                st.json(data)
                st.download_button("Download", json.dumps(data, indent=2), f.name)
    else:
        st.info("No history yet.")

