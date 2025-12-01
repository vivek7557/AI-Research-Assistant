"""
streamlit_wrapper.py

Final merged file:
- UI matches the screenshot (gradient header, hero, search bar, pills)
- Original research logic preserved (ResearchOrchestrator, ResearchEvaluator, MemoryBank)
- Tabs, evaluation, downloads unchanged
"""

import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

# --- Core logic modules (unchanged) ---
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
# Screenshot-accurate UI CSS + HTML (top of file)
# ======================================================
st.markdown("""
<style>
:root {
    --gradient-1: #0f0b2c;
    --gradient-2: #3a185f;
    --gradient-3: #6b2a99;
    --accent-a: #4ff0ff;
    --accent-b: #bf6afc;
    --glass: rgba(255,255,255,0.04);
    --glass-2: rgba(255,255,255,0.06);
    --border: rgba(255,255,255,0.08);
}

html, body, .block-container {
    background: linear-gradient(135deg, var(--gradient-1), var(--gradient-2), var(--gradient-3)) !important;
}

/* Top nav bar */
.topbar {
    width: 100%;
    padding: 14px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(90deg, rgba(0,0,0,0.05), rgba(255,255,255,0.03));
    border-bottom: 1px solid rgba(255,255,255,0.02);
    margin-bottom: 18px;
    border-radius: 6px;
}

/* Logo */
.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    color: white;
    font-weight: 700;
    font-size: 1.05rem;
}
.logo .dot {
    width: 28px;
    height: 28px;
    border-radius: 8px;
    background: linear-gradient(90deg, #4ff0ff, #bf6afc);
    display: inline-block;
}

/* Hero */
.hero {
    text-align: center;
    padding: 48px 20px 24px 20px;
}

.hero h1 {
    margin: 0;
    font-size: 36px;
    font-weight: 900;
    color: white;
}

.hero h1 .highlight {
    background: linear-gradient(90deg, var(--accent-a), var(--accent-b));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p.sub {
    margin-top: 10px;
    color: rgba(227, 231, 240, 0.9);
    font-size: 14px;
}

/* Search container (glass) */
.search-container {
    margin: 18px auto 6px auto;
    max-width: 820px;
    background: rgba(255,255,255,0.03);
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.06);
    padding: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    backdrop-filter: blur(6px);
}

/* Input style provided to Streamlit control by overriding */
.search-container .stTextInput > div > div > input {
    background: transparent !important;
    color: #f8fafc !important;
    border: none !important;
    outline: none !important;
    font-size: 14px !important;
    padding-left: 8px !important;
}

/* Research button */
.search-btn > button {
    background: linear-gradient(90deg, #3fb3ff, #994bff) !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 8px 18px !important;
    border-radius: 10px !important;
}

/* Pills */
.pills {
    margin-top: 12px;
    text-align: center;
}
.pill {
    display: inline-block;
    margin: 6px 6px;
    padding: 6px 14px;
    border-radius: 20px;
    background: rgba(255,255,255,0.03);
    color: #e6eef8;
    font-size: 13px;
    border: 1px solid rgba(255,255,255,0.05);
}

/* Responsive adjustments */
@media (max-width: 900px) {
    .hero h1 { font-size: 28px; }
    .search-container { max-width: 92%; padding: 10px; }
}
</style>
""", unsafe_allow_html=True)

# Top nav bar (logo + small right-side spacer)
st.markdown("""
<div class="topbar">
    <div class="logo">
        <div class="dot"></div>
        <div>ResearchAI</div>
    </div>
    <div style="opacity:0.6; font-size:13px; color:#dbeafe"> </div>
</div>
""", unsafe_allow_html=True)


# Hero text (screenshot style)
st.markdown("""
<div class="hero">
    <h1>Deep Research at <span class="highlight">Lightning Speed</span></h1>
    <p class="sub">Powered by advanced AI agents. Get comprehensive, verified research in minutes, not hours.</p>
</div>
""", unsafe_allow_html=True)


# Search UI block (glass)
st.markdown("<div class='search-container'>", unsafe_allow_html=True)

col_left, col_right = st.columns([8, 2], gap="small")

with col_left:
    # This input will be used by the existing logic (query variable)
    query = st.text_input(
        "", 
        placeholder="E.g., Impact of AI on healthcare, Climate solutions, Quantum computing...",
        label_visibility="collapsed",
        key="ui_search_query"
    )

with col_right:
    # This button will be the trigger; we'll use this boolean in the tabs logic
    do_search = st.button("Research", key="ui_search_btn", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Pills row
st.markdown("""
<div class="pills">
    <span class="pill">Renewable Energy</span>
    <span class="pill">Drug Discovery</span>
    <span class="pill">Space Exploration</span>
    <span class="pill">Cybersecurity</span>
</div>
""", unsafe_allow_html=True)

# Save button state for use in the rest of the app (so existing logic can read it)
# Keep the session state key consistent so existing flow can be wired easily.
st.session_state["ui_search_trigger"] = do_search

# ======================================================
# Sidebar: statistics and recent activity (keeps logic)
# ======================================================
with st.sidebar:
    st.markdown("### 📊 Research Analytics")
    try:
        memory_bank = MemoryBank()
        stats = memory_bank.get_statistics()

        st.metric("Total Research", stats.get("total_memories", 0))
        st.metric("Completed", stats.get("completed_sessions", 0))
        st.metric("Total Sources", stats.get("total_sources", 0))
        st.metric("Avg Quality", f"{stats.get('avg_importance', 0):.1f}/10")
    except Exception:
        st.info("Statistics will appear after first research")

    st.markdown("---")
    st.markdown("### Recent Activity")
    output_dir = Path("outputs")
    if output_dir.exists():
        json_files = list(output_dir.glob("*.json"))
        if json_files:
            recent_files = sorted(json_files, key=os.path.getmtime, reverse=True)[:6]
            for file in recent_files:
                try:
                    with open(file, "r") as f:
                        d = json.load(f)
                    st.write("• " + d.get("query", "Untitled")[:40] + "...")
                except Exception:
                    pass
        else:
            st.info("No recent activity")
    else:
        st.info("No activity yet")


# ======================================================
# API Keys (unchanged)
# ======================================================
anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "")

if anthropic_key:
    os.environ["ANTHROPIC_API_KEY"] = anthropic_key
if tavily_key:
    os.environ["TAVILY_API_KEY"] = tavily_key

if not (anthropic_key and tavily_key):
    st.error("⚠️ API Keys missing. Please configure ANTHROPIC_API_KEY and TAVILY_API_KEY in .env or Streamlit secrets.")
    st.stop()


# ======================================================
# Tabs & rest of logic (preserved)
# ======================================================
tab1, tab2, tab3 = st.tabs(["🔬 New Research", "🔍 Find Related", "📂 Past Sessions"])

# Tab 1 - New Research (logic preserved)
with tab1:
    st.markdown("## 🔬 New Research")

    col_format, col_eval = st.columns([3, 2])
    with col_format:
        output_format = st.selectbox("📄 Output Format", ["report", "article", "summary", "presentation"])
    with col_eval:
        run_evaluation = st.checkbox("🎯 Run Evaluation", value=True)

    with st.expander("⚙️ Advanced Options"):
        colA, colB = st.columns(2)
        with colA:
            session_id_input = st.text_input("Resume Session ID", placeholder="research_xxxxx")
        with colB:
            depth_level = st.slider("Research Depth", 1, 5, 3)

    # The trigger for starting research: either the UI search button at top or the "Start Research" here.
    start_trigger = st.session_state.get("ui_search_trigger", False) or st.button("🚀 Start Research", use_container_width=False)

    if start_trigger:
        # Use the query value from the UI search input
        q = query if query else ""
        if not q:
            st.warning("⚠️ Please enter a research query")
            st.stop()

        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            status_text.info("🎯 Initializing research agents...")
            progress_bar.progress(20)
            orchestrator = ResearchOrchestrator()

            status_text.info("📋 Planning research strategy...")
            progress_bar.progress(40)

            status_text.info("🔍 Conducting research...")
            progress_bar.progress(60)

            # Call unchanged orchestrator function; pass output_format and session_id similar to prior logic
            results = orchestrator.conduct_research(
                query=q,
                output_format=output_format,
                session_id=session_id_input or None
            )

            status_text.info("✅ Finalizing report...")
            progress_bar.progress(100)

            progress_bar.empty()
            status_text.empty()
            st.success("✅ Research completed successfully!")

            # Metrics
            st.markdown("---")
            st.markdown('<div style="font-weight:700; font-size:18px; margin-bottom:8px;">📊 Research Metrics</div>', unsafe_allow_html=True)

            final_content = results.get("final_content", {})
            summary = results.get("research_summary", {})
            validation = results.get("validation", {})

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📚 Sources", summary.get("total_sources", 0))
            col2.metric("🔄 Iterations", summary.get("iterations", 0))
            col3.metric("🎯 Confidence", f"{validation.get('confidence_score', 0)}%")
            col4.metric("📝 Format", output_format.title())

            # Content
            st.markdown("---")
            st.markdown('<div style="font-weight:700; font-size:18px; margin-bottom:8px;">📄 Generated Research</div>', unsafe_allow_html=True)

            content = final_content.get("content", "")
            if not content:
                st.warning(f"⚠️ No {output_format} content generated. This may be an orchestrator issue.")
                st.info("💡 Make sure your orchestrator.conduct_research() returns content for all formats.")
            else:
                st.markdown(content, unsafe_allow_html=True)

            # Downloads
            st.markdown("---")
            d1, d2, d3 = st.columns(3)
            d1.download_button("📥 Download Markdown", data=content, file_name="research.md", use_container_width=True)
            d2.download_button("📥 Download JSON", data=json.dumps(results, indent=2), file_name="research.json", use_container_width=True)
            d3.download_button("📥 Download TXT", data=content, file_name="research.txt", use_container_width=True)

            # Evaluation
            if run_evaluation:
                st.markdown("---")
                st.markdown('<div style="font-weight:700; font-size:18px; margin-bottom:8px;">📊 Quality Evaluation</div>', unsafe_allow_html=True)

                try:
                    evaluator = ResearchEvaluator()
                    metrics = evaluator.evaluate_research(q, results)
                    metrics_dict = metrics.to_dict()

                    explanations = {
                        "completeness": "Measures how fully the research covers all important aspects of the topic.",
                        "accuracy": "Checks factual correctness based on cross-verified sources.",
                        "relevance": "Evaluates how closely content matches the research query.",
                        "quality": "Judges structure, clarity, and flow of writing.",
                        "efficiency": "Measures how well sources were used to produce concise content.",
                        "citations": "Evaluates whether sources are properly referenced.",
                    }

                    for metric, score in metrics_dict.items():
                        m_name = metric.replace("_", " ").title()
                        st.markdown(f"<div style='padding:12px; border-radius:8px; background:rgba(255,255,255,0.02); margin-bottom:8px;'><strong>{m_name}:</strong> {score:.0f}</div>", unsafe_allow_html=True)
                        st.progress(score / 100)

                    st.markdown("---")
                    overall = metrics.overall_score
                    emoji = "🟢" if overall >= 80 else "🟡" if overall >= 60 else "🔴"
                    st.markdown(f"<div style='padding:12px; border-radius:8px; background:rgba(255,255,255,0.02);'><strong>{emoji} Overall Quality Score: {overall:.1f}/100</strong></div>", unsafe_allow_html=True)

                except Exception as e:
                    st.warning(f"Evaluation unavailable: {str(e)}")

        except Exception as e:
            st.error(f"❌ Research failed: {str(e)}")
            with st.expander("Show error details"):
                st.exception(e)

# Tab 2 - Find Related
with tab2:
    st.markdown("## 🔍 Find Related Research")
    st.markdown("Enter keywords to find sessions that match or are similar to your topic.")
    related_query = st.text_input("Search Query", placeholder="Enter keywords or topic to find related research", key="related_query_input")

    if st.button("🔎 Search Related"):
        if related_query:
            try:
                memory_bank = MemoryBank()
                related = memory_bank.get_related_research(related_query, limit=10)

                if related:
                    st.success(f"✅ Found {len(related)} related research sessions")
                    for i, session in enumerate(related, 1):
                        with st.expander(f"📄 {session.get('query', 'Untitled')}"):
                            col1, col2 = st.columns(2)
                            col1.write("**Session:**", session.get('id', 'N/A')[:12] + "...")
                            col2.write("**Sources:**", session.get('sources_count', 0))
                else:
                    st.info("No related research found. Try different keywords.")
            except Exception as e:
                st.error(f"Search failed: {str(e)}")
        else:
            st.warning("Please enter a search query")

# Tab 3 - Past Sessions
with tab3:
    st.markdown("## 📂 Past Research Sessions")
    output_dir = Path("outputs")
    if output_dir.exists():
        json_files = list(output_dir.glob("*.json"))
        if json_files:
            st.info(f"📊 {len(json_files)} research sessions found")
            sorted_files = sorted(json_files, key=os.path.getmtime, reverse=True)
            for json_file in sorted_files[:20]:
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                    query_text = data.get('query', 'Untitled')
                    with st.expander(f"📄 {query_text}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**ID:**", data.get('session_id', 'N/A')[:12] + "...")
                            st.write("**Format:**", data.get('output_format', 'N/A'))
                        with col2:
                            summary = data.get('research_summary', {})
                            st.write("**Sources:**", summary.get('total_sources', 0))
                            st.write("**Iterations:**", summary.get('iterations', 0))
                        st.download_button("📥 Download", json.dumps(data, indent=2), json_file.name, use_container_width=True)
                except Exception as e:
                    st.error(f"Error loading {json_file.name}")
        else:
            st.info("📭 No past sessions found. Start your first research!")
    else:
        st.info("📭 No research history yet.")

# Footer
st.markdown("""
<div style="text-align:center; color:rgba(235,235,245,0.8); padding:22px 0;">
    <strong>AI Research Assistant</strong> • Multi-Agent System • Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
