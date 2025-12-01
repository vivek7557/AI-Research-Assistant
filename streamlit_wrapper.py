"""
streamlit_wrapper.py — MODERN GLASS-MORPHISM UI
Logic 100 % unchanged.
"""
import streamlit as st
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

# --------------------------------------------------
# Core logic (unchanged)
# --------------------------------------------------
from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator
from memory.memory_bank import MemoryBank

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Minimal glass-morphism CSS
# --------------------------------------------------
st.markdown(
    """
<style>
:root {
    --bg0: #0c0c0f;
    --bg1: #111115;
    --bg2: #1a1a20;
    --glass: rgba(26, 26, 32, 0.55);
    --accent: #00f5ff;
    --accent2: #ff00c1;
    --text: #f0f0f5;
    --text2: #a0a0b3;
    --border: rgba(255, 255, 255, 0.08);
    --radius: 12px;
    --blur: 16px;
    --font: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

html, body, .block-container {
    background: var(--bg0);
    font-family: var(--font);
    color: var(--text);
}

/* Glass card */
.glass {
    background: var(--glass);
    backdrop-filter: blur(var(--blur));
    -webkit-backdrop-filter: blur(var(--blur));
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* Inputs */
.stTextInput input, .stSelectbox select {
    background: var(--bg1);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    padding: 0.5rem 0.75rem;
}
.stTextInput input:focus, .stSelectbox select:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent);
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    color: #fff;
    border: none;
    border-radius: var(--radius);
    padding: 0.5rem 1.25rem;
    font-weight: 600;
}
.stButton > button:hover {
    transform: scale(1.03);
}

/* Metric */
.metric-card {
    text-align: center;
    padding: 1rem;
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: var(--radius);
}
.metric-value {
    font-size: 2rem;
    font-weight: 600;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-label {
    font-size: 0.8rem;
    color: var(--text2);
    margin-top: 0.25rem;
}
</style>""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown("### 📊 Research Analytics")
    try:
        stats = MemoryBank().get_statistics()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{stats.get("total_memories",0)}</div><div class="metric-label">Total Research</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{stats.get("completed_sessions",0)}</div><div class="metric-label">Completed</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{stats.get("total_sources",0)}</div><div class="metric-label">Sources</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{stats.get("avg_importance",0):.1f}</div><div class="metric-label">Avg Quality</div></div>',
                unsafe_allow_html=True,
            )
    except Exception:
        st.info("Stats will appear after first research.")

    st.markdown("### Recent Activity")
    out = Path("outputs")
    if out.exists():
        files = sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)[:6]
        for f in files:
            try:
                q = json.loads(f.read_text()).get("query", "Untitled")
                st.markdown(f"• {q[:40]}…")
            except Exception:
                pass
    else:
        st.markdown("No activity yet")

# --------------------------------------------------
# API keys
# --------------------------------------------------
anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "")
if anthropic_key:
    os.environ["ANTHROPIC_API_KEY"] = anthropic_key
if tavily_key:
    os.environ["TAVILY_API_KEY"] = tavily_key
keys_set = bool(anthropic_key and tavily_key)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown("## 🔬 ResearchAI")
st.markdown("Deep, multi-agent research at your fingertips.")

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs(["New Research", "Find Related", "Past Sessions"])

# ---------- New Research ----------
with tab1:
    if not keys_set:
        st.error("Add ANTHROPIC_API_KEY and TAVILY_API_KEY to .env or secrets")
        st.stop()

    with st.form("research_form"):
        query = st.text_input("Research Query", placeholder="E.g. Impact of AI on healthcare")
        col_format, col_eval = st.columns([3, 2])
        with col_format:
            output_format = st.selectbox("Output Format", ["report", "article", "summary", "presentation"])
        with col_eval:
            run_evaluation = st.checkbox("Run Evaluation", value=True)
        with st.expander("Advanced"):
            session_id_input = st.text_input("Resume Session ID", placeholder="research_xxxxx")
            depth_level = st.slider("Research Depth", 1, 5, 3)
        submitted = st.form_submit_button("Start Research", use_container_width=True)

    if submitted and query:
        progress = st.progress(0)
        status = st.empty()
        try:
            status.info("Initializing agents…")
            progress.progress(20)
            orch = ResearchOrchestrator()

            status.info("Planning strategy…")
            progress.progress(40)

            status.info("Conducting research…")
            progress.progress(60)
            results = orch.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None,
            )

            status.info("Finalising report…")
            progress.progress(100)
            time.sleep(0.3)
            progress.empty()
            status.empty()
            st.success("Research completed!")

            summary = results.get("research_summary", {})
            validation = results.get("validation", {})
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Sources", summary.get("total_sources", 0))
            c2.metric("Iterations", summary.get("iterations", 0))
            c3.metric("Confidence", f"{validation.get('confidence_score', 0)}%")
            c4.metric("Format", output_format.title())

            content = results.get("final_content", {}).get("content", "")
            st.markdown(content)

            d1, d2, d3 = st.columns(3)
            d1.download_button("Markdown", data=content, file_name="research.md", use_container_width=True)
            d2.download_button("JSON", data=json.dumps(results, indent=2), file_name="research.json", use_container_width=True)
            d3.download_button("TXT", data=content, file_name="research.txt", use_container_width=True)

            if run_evaluation:
                evaluator = ResearchEvaluator()
                metrics = evaluator.evaluate_research(query, results)
                overall = metrics.overall_score
                st.markdown("---")
                st.markdown(f"**Quality Score:** {overall:.1f}/100")
                for k, v in metrics.to_dict().items():
                    st.write(f"{k.replace('_', ' ').title()} – {v:.0f}/100")
                    st.progress(v / 100)

        except Exception as e:
            st.error(f"Research failed: {e}")
            with st.expander("Traceback"):
                st.exception(e)

# ---------- Find Related ----------
with tab2:
    related_query = st.text_input("Search Query", placeholder="Keywords or topic")
    if st.button("Search"):
        if related_query:
            try:
                related = MemoryBank().get_related_research(related_query, limit=10)
                if related:
                    st.success(f"Found {len(related)} related sessions")
                    for r in related:
                        with st.expander(r.get("query", "Untitled")):
                            st.write("ID:", r.get("id", "N/A")[:12] + "…")
                            st.write("Sources:", r.get("sources_count", 0))
                else:
                    st.info("No matches – try different keywords.")
            except Exception as e:
                st.error(f"Search failed: {e}")

# ---------- Past Sessions ----------
with tab3:
    out = Path("outputs")
    if out.exists():
        files = sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)
        st.metric("Total sessions", len(files))
        for f in files[:20]:
            try:
                data = json.loads(f.read_text())
                with st.expander(data.get("query", "Untitled")):
                    c1, c2 = st.columns(2)
                    c1.write("**ID:** " + data.get("session_id", "N/A")[:12] + "…")
                    summary = data.get("research_summary", {})
                    c2.write("**Sources:** " + str(summary.get("total_sources", 0)))
                    st.download_button("Download", json.dumps(data, indent=2), f.name, use_container_width=True)
            except Exception:
                pass
    else:
        st.info("No history yet.")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-size:0.8rem;color:var(--text2);">'
    "Built with ❤️ using Streamlit • Multi-Agent Research AI</div>",
    unsafe_allow_html=True,
)
