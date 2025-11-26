"""
Streamlit Web Interface for AI Research Assistant
Modern UI with centered layout and comprehensive analysis
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

# Custom CSS - Lighter, colorful, compact React-style UI
st.markdown("""
<style>

/* ====================================== */
/*         LIGHT & COLORFUL ANIMATIONS    */
/* ====================================== */

@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(6px); }
    100% { opacity: 1; transform: translateY(0); }
}
.fade-in {
    animation: fadeInUp 0.45s ease both;
}

.main-header,
.input-container,
.content-card {
    animation: fadeInUp 0.45s ease both;
}

.section-block {
    opacity: 0;
    animation: fadeInUp 0.6s ease forwards;
}
.section-block:nth-child(1) { animation-delay: 0.05s; }
.section-block:nth-child(2) { animation-delay: 0.1s; }
.section-block:nth-child(3) { animation-delay: 0.15s; }

/* Soft glow on hover */
@keyframes softGlow {
    from { box-shadow: 0 0 0 rgba(129, 140, 248, 0); }
    to { box-shadow: 0 0 10px rgba(129, 140, 248, 0.2); }
}
.input-container:hover,
.content-card:hover,
.eval-right:hover {
    animation: softGlow 0.3s ease forwards;
    border-color: #818cf8;
}

/* Gradient header - refreshed colors */
@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}
.main-header h1 {
    font-size: 1.95rem;
    font-weight: 700;
    background: linear-gradient(120deg, #818cf8, #c084fc);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientFlow 6s ease-in-out infinite alternate;
}

/* Thinner progress */
.stProgress > div > div {
    height: 5px !important;
    background-color: #818cf8 !important;
    animation: pulseBar 2s ease-in-out infinite;
}
@keyframes pulseBar {
    0%, 100% { opacity: 0.7; }
    50% { opacity: 1; }
}

/* Evaluation slide */
@keyframes slideInRight {
    0% { opacity: 0; transform: translateX(10px); }
    100% { opacity: 1; transform: translateX(0); }
}
.eval-right {
    animation: slideInRight 0.4s ease both;
}


/* ====================================== */
/*           LIGHT BUTTONS & CONTROLS     */
/* ====================================== */

/* Primary Action Button - LIGHTER & SMALLER */
.stButton > button {
    height: 2.3rem !important;
    padding: 0 1.25rem !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    background: linear-gradient(to right, #6366f1, #8b5cf6) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 2px 6px rgba(99, 102, 241, 0.25) !important;
    transition: all 0.18s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(99, 102, 241, 0.35) !important;
    background: linear-gradient(to right, #4f46e5, #7c3aed) !important;
}

/* Download Buttons - subtle & small */
.stDownloadButton > button {
    height: 2.2rem !important;
    font-size: 0.85rem !important;
    padding: 0 1.1rem !important;
    border-radius: 6px !important;
    background: #1e293b !important;
    color: #cbd5e1 !important;
    border: 1px solid #334155 !important;
    transition: all 0.15s ease;
}
.stDownloadButton > button:hover {
    background: #334155 !important;
    color: white !important;
    transform: translateY(-1px);
    border-color: #475569 !important;
}

/* Tabs - colorful & compact */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.7rem;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    background: #1e293b !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: 8px !important;
    border: 1px solid #334155 !important;
    font-weight: 600;
    font-size: 0.92rem !important;
    color: #cbd5e1 !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #334155 !important;
    border-color: #818cf8 !important;
    color: white !important;
    box-shadow: 0 2px 6px rgba(129, 140, 248, 0.2) !important;
}

/* Inputs - light border, clean */
input, textarea, select {
    font-size: 0.92rem !important;
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    color: #e2e8f0 !important;
    border-radius: 6px !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    padding: 0.5rem 0.75rem !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 7px !important;
    padding: 0.4rem 0.8rem !important;
    font-size: 0.92rem !important;
    color: #cbd5e1 !important;
}


/* ====================================== */
/*           BASE STYLING (COLORFUL)      */
/* ====================================== */

.main-content {
    max-width: 1080px;
    margin: auto;
    padding: 1.4rem;
}

.main-header {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.25);
}

.main-header p {
    font-size: 0.98rem;
    color: #94a3b8;
    margin-top: 0.4rem;
}

.input-container {
    background: #0f172a;
    border: 1px solid #1e293b;
    padding: 1.2rem;
    border-radius: 12px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.28);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0b111f !important;
    border-right: 1px solid #1e293b;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #0f172a;
    padding: 0.8rem;
    border: 1px solid #1e293b;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    height: 76px;
}

/* Content card */
.content-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    padding: 0.95rem;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}

/* Evaluation score */
.eval-title {
    font-size: 0.78rem;
    color: #94a3b8;
}
.eval-score {
    font-size: 1.35rem;
    font-weight: 700;
    color: #e2e8f0;
}

</style>
""", unsafe_allow_html=True)

# Sidebar styling (compact + colorful)
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: #0b111f !important;
    padding: 1rem 0.7rem !important;
}

.sidebar-card {
    background: #121d2f;
    border: 1px solid #1e293b;
    border-radius: 9px;
    padding: 0.65rem 0.85rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.sidebar-title {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-bottom: 3px;
}

.sidebar-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: #e2e8f0;
}

.sidebar-activity-title {
    margin-top: 1.2rem;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    color: #cbd5e1;
}

.sidebar-activity-item {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-bottom: 4px;
}

.sidebar-activity-item:hover {
    color: #e2e8f0;
    margin-left: 2px;
}
</style>
""", unsafe_allow_html=True)


# =============== REST OF YOUR CODE UNCHANGED ===============

# Sidebar
with st.sidebar:

    st.markdown("### 📊 Research Analytics")

    # Memory stats
    try:
        memory_bank = MemoryBank()
        stats = memory_bank.get_statistics()

        st.markdown(f"""
        <div class="sidebar-card">
            <div class="sidebar-title">📚 Total Research</div>
            <div class="sidebar-value">{stats.get('total_memories', 0)}</div>
        </div>

        <div class="sidebar-card">
            <div class="sidebar-title">✅ Completed</div>
            <div class="sidebar-value">{stats.get('completed_sessions', 0)}</div>
        </div>

        <div class="sidebar-card">
            <div class="sidebar-title">🔗 Total Sources</div>
            <div class="sidebar-value">{stats.get('total_sources', 0)}</div>
        </div>

        <div class="sidebar-card">
            <div class="sidebar-title">⭐ Avg Quality</div>
            <div class="sidebar-value">{stats.get('avg_importance', 0):.1f}/10</div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.info("Statistics will appear after first research")

    st.markdown("<div class='sidebar-activity-title'>📝 Recent Activity</div>", unsafe_allow_html=True)

    # Recent Activity
    output_dir = Path("outputs")
    if output_dir.exists():
        json_files = list(output_dir.glob("*.json"))

        if json_files:
            recent_files = sorted(json_files, key=os.path.getmtime, reverse=True)[:6]
            for file in recent_files:
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    query = data.get("query", "Untitled")

                    st.markdown(
                        f"<div class='sidebar-activity-item'>• {query[:32]}...</div>",
                        unsafe_allow_html=True
                    )

                except:
                    pass
        else:
            st.markdown("<div class='sidebar-activity-item'>No recent activity</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='sidebar-activity-item'>No activity yet</div>", unsafe_allow_html=True)


# API Keys
try:
    anthropic_key = st.secrets["ANTHROPIC_API_KEY"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    tavily_key = st.secrets["TAVILY_API_KEY"]
    keys_set = True
except KeyError:
    keys_set = False


# Main Container
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🔍 AI Research Assistant</h1>
    <p>Deep research powered by multi-agent AI system</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔬 New Research", "🔍 Find Related", "📂 Past Sessions"])

# Tab 1 - New Research
with tab1:
    if not keys_set:
        st.error("⚠️ API Keys missing in .env")
        st.stop()

    col1, col2, col3 = st.columns([1, 8, 1])

    with col2:
        st.markdown('<div class="input-container">', unsafe_allow_html=True)

        query = st.text_input(
            "🔎 Research Query",
            placeholder="e.g., Impact of artificial intelligence on healthcare",
            label_visibility="collapsed"
        )

        col_format, col_eval = st.columns([3, 2])
        output_format = col_format.selectbox("📄 Output Format",
                                             ["report", "article", "summary", "presentation"])
        run_evaluation = col_eval.checkbox("🎯 Run Evaluation", value=True)

        with st.expander("⚙️ Advanced Options"):
            colA, colB = st.columns(2)
            session_id_input = colA.text_input("Resume Session ID", placeholder="research_xxxx")
            depth_level = colB.slider("Research Depth", 1, 5, 3)

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🚀 Start Research", use_container_width=True):
            if not query:
                st.warning("Please enter a research query.")
                st.stop()

            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                status_text.info("Initializing...")
                progress_bar.progress(20)
                orchestrator = ResearchOrchestrator()

                status_text.info("Planning research...")
                progress_bar.progress(40)

                status_text.info("Running agents...")
                progress_bar.progress(60)
                results = orchestrator.conduct_research(
                    query=query,
                    output_format=output_format,
                    session_id=session_id_input or None,
                )

                status_text.info("Finalizing...")
                progress_bar.progress(100)

                progress_bar.empty()
                status_text.empty()

                st.success("✅ Research completed successfully!")

                st.markdown("---")
                st.markdown("### 📊 Research Metrics")

                final_content = results.get("final_content", {})
                summary = results.get("research_summary", {})
                validation = results.get("validation", {})

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("📚 Sources", summary.get("total_sources", 0))
                col2.metric("🔄 Iterations", summary.get("iterations", 0))
                col3.metric("🎯 Confidence", f"{validation.get('confidence_score', 0)}%")
                col4.metric("📝 Format", output_format.title())

                st.markdown("---")
                st.markdown("### 📄 Generated Research")

                content = final_content.get("content", "")
                st.markdown(content)

                st.markdown("---")
                d1, d2, d3 = st.columns(3)
                d1.download_button("📥 Markdown", data=content, file_name="research.md")
                d2.download_button(
                    "📥 JSON",
                    data=json.dumps(results, indent=2),
                    file_name="research.json",
                )
                d3.download_button("📥 TXT", data=content, file_name="research.txt")

                # Evaluation Section
                if run_evaluation:
                    st.markdown("---")
                    st.markdown("### 📊 Quality Evaluation")

                    try:
                        evaluator = ResearchEvaluator()
                        metrics = evaluator.evaluate_research(query, results)
                        metrics_dict = metrics.to_dict()

                        explanations = {
                            "completeness": "Measures how fully the research covers all important aspects of the topic. Higher score means minimal missing information.",
                            "accuracy": "Checks how factually correct the statements are, based on cross-verified sources.",
                            "relevance": "Evaluates how closely the content matches the research query and avoids unrelated details.",
                            "quality": "Judges structure, clarity, and flow of writing. Higher means well-organized research.",
                            "efficiency": "Measures how well the system used sources and produced concise, high-value content.",
                            "citations": "Evaluates whether sources are properly referenced and credible.",
                            "overall": "This is the weighted average of all metrics — your total research quality score.",
                        }

                        for metric, score in metrics_dict.items():
                            m_name = metric.replace("_", " ").title()

                            left, right = st.columns([4, 1])

                            with left:
                                st.markdown(f"**{m_name}**")
                                st.progress(score / 100)
                                st.markdown(
                                    f"<p style='font-size:0.85rem; color:#94a3b8; margin-top:4px;'>"
                                    f"{explanations.get(metric, '')}</p>",
                                    unsafe_allow_html=True,
                                )

                            with right:
                                st.markdown(
                                    f"""
<div class="eval-right">
    <div class="eval-title">{m_name}</div>
    <div class="eval-score">{score}</div>
</div>
""",
                                    unsafe_allow_html=True,
                                )

                        st.markdown("---")
                        overall = metrics.overall_score
                        emoji = "🟢" if overall >= 80 else "🟡" if overall >= 60 else "🔴"
                        st.markdown(
                            f"""
<h3>{emoji} Overall Quality Score: {overall:.1f}/100</h3>
<p style='color:#94a3b8; font-size:0.9rem;'>
{explanations['overall']}
</p>
""",
                            unsafe_allow_html=True,
                        )
                    except Exception as e:
                        st.warning(f"Evaluation unavailable: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error during research: {str(e)}")

# Tabs 2 & 3 unchanged
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; opacity:0.7; padding:1rem; color: #94a3b8;'>
    AI Research Assistant v2.0 • Multi-Agent System<br>
    Powered by Claude & Tavily
</div>
""", unsafe_allow_html=True)
