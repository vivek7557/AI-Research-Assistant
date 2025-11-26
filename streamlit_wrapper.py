"""
Streamlit Web Interface for AI Research Assistant
Premium UI - Clean, Modern, Professional
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

# PREMIUM UI CSS - CLEAN & MODERN
st.markdown("""
<style>

/* ==================== GLOBAL STYLES ==================== */

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideInLeft { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
@keyframes glow { 0%, 100% { box-shadow: 0 0 15px rgba(59, 130, 246, 0.4); } 50% { box-shadow: 0 0 30px rgba(59, 130, 246, 0.7); } }
@keyframes shimmer { 0% { background-position: -1000px 0; } 100% { background-position: 1000px 0; } }

/* Base Theme */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e27 0%, #16213e 50%, #0f3460 100%) !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f3460 0%, #16213e 100%) !important;
    border-right: 1px solid rgba(59, 130, 246, 0.2) !important;
}

/* ==================== BUTTONS ==================== */

.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%) !important;
    border: 1px solid rgba(59, 130, 246, 0.5) !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    height: 40px !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.35) !important;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.6) !important;
    border-color: rgba(59, 130, 246, 0.8) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Download Buttons */
.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border: 1px solid rgba(16, 185, 129, 0.5) !important;
    color: white !important;
    font-weight: 700 !important;
    height: 40px !important;
    padding: 10px 24px !important;
    font-size: 13px !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 20px rgba(16, 185, 129, 0.35) !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(16, 185, 129, 0.6) !important;
}

/* ==================== INPUTS ==================== */

input, select {
    background: rgba(15, 52, 96, 0.4) !important;
    border: 1px solid rgba(59, 130, 246, 0.4) !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    padding: 10px 14px !important;
    font-size: 13px !important;
    transition: all 0.3s !important;
}

input::placeholder { color: rgba(203, 213, 225, 0.5) !important; }

input:focus, select:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    background: rgba(15, 52, 96, 0.6) !important;
}

/* ==================== HEADER ==================== */

.main-header {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%) !important;
    border: 1px solid rgba(59, 130, 246, 0.35) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px) !important;
    animation: slideInLeft 0.6s ease-out;
}

.main-header h1 {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-size: 28px !important;
    margin: 0 !important;
    font-weight: 800 !important;
}

.main-header p {
    font-size: 13px !important;
    color: #a5b4fc !important;
    margin-top: 8px !important;
}

/* ==================== CARDS ==================== */

.input-container {
    background: linear-gradient(135deg, rgba(22, 33, 62, 0.6) 0%, rgba(15, 52, 96, 0.6) 100%) !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.12) !important;
    backdrop-filter: blur(10px) !important;
    animation: fadeIn 0.7s ease-out;
}

.input-container:hover {
    border-color: rgba(59, 130, 246, 0.5) !important;
    box-shadow: 0 12px 32px rgba(59, 130, 246, 0.2) !important;
}

.content-card {
    background: linear-gradient(135deg, rgba(22, 33, 62, 0.6) 0%, rgba(15, 52, 96, 0.6) 100%) !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.12) !important;
    backdrop-filter: blur(10px) !important;
}

.content-card:hover {
    border-color: rgba(59, 130, 246, 0.5) !important;
}

/* ==================== TABS ==================== */

.stTabs [data-baseweb="tab-list"] {
    gap: 12px !important;
    border-bottom: 1px solid rgba(59, 130, 246, 0.2) !important;
    padding-bottom: 14px !important;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(59, 130, 246, 0.08) !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 8px !important;
    padding: 10px 18px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    color: #cbd5e1 !important;
    transition: all 0.3s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    border-color: rgba(59, 130, 246, 0.6) !important;
    background: rgba(59, 130, 246, 0.15) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    border-color: #3b82f6 !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
}

/* ==================== METRICS ==================== */

[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.08) 100%) !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.12) !important;
    transition: all 0.3s ease !important;
    animation: fadeIn 0.6s ease-out;
}

[data-testid="stMetric"]:hover {
    border-color: rgba(59, 130, 246, 0.5) !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.25) !important;
}

[data-testid="stMetric"] label {
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #a5b4fc !important;
}

[data-testid="stMetric"] div {
    font-size: 20px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

/* ==================== PROGRESS ==================== */

.stProgress > div > div > div {
    background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 25%, #06b6d4 50%, #10b981 75%, #f59e0b 100%) !important;
    background-size: 200% 100%;
    animation: shimmer 2.5s infinite;
}

.stProgress > div > div {
    background: rgba(59, 130, 246, 0.1) !important;
    border-radius: 10px !important;
}

/* ==================== SIDEBAR ==================== */

.sidebar-card {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%) !important;
    border: 1px solid rgba(59, 130, 246, 0.35) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.12) !important;
    transition: all 0.3s ease !important;
    animation: slideInLeft 0.6s ease-out;
    margin-bottom: 12px !important;
}

.sidebar-card:hover {
    border-color: rgba(59, 130, 246, 0.6) !important;
    transform: translateX(4px) translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2) !important;
}

.sidebar-title {
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #a5b4fc !important;
    margin-bottom: 8px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.sidebar-value {
    font-size: 20px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sidebar-activity-title {
    font-size: 12px !important;
    font-weight: 800 !important;
    color: #f1f5f9 !important;
    margin-top: 16px !important;
    margin-bottom: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.sidebar-activity-item {
    font-size: 12px !important;
    color: #a5b4fc !important;
    padding: 8px 10px !important;
    margin-bottom: 8px !important;
    border-left: 3px solid rgba(59, 130, 246, 0.5) !important;
    padding-left: 12px !important;
    transition: all 0.2s ease !important;
    border-radius: 4px !important;
    background: rgba(59, 130, 246, 0.05) !important;
}

.sidebar-activity-item:hover {
    color: #3b82f6 !important;
    border-left-color: #3b82f6 !important;
    background: rgba(59, 130, 246, 0.15) !important;
}

/* ==================== ALERTS ==================== */

[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-size: 13px !important;
    border-left: 4px solid !important;
    padding: 14px 16px !important;
    backdrop-filter: blur(10px) !important;
    animation: fadeIn 0.4s ease-out;
}

/* ==================== EXPANDER ==================== */

[data-testid="stExpander"] {
    border-radius: 10px !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.05)) !important;
}

[data-testid="stExpander"] > div > button {
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #a5b4fc !important;
}

[data-testid="stExpander"] > div > button:hover {
    background: rgba(59, 130, 246, 0.1) !important;
}

/* ==================== EVAL CARDS ==================== */

.eval-right {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%) !important;
    border: 1px solid rgba(59, 130, 246, 0.4) !important;
    border-radius: 10px !important;
    padding: 14px !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
    animation: fadeIn 0.5s ease-out;
}

.eval-right:hover {
    border-color: rgba(59, 130, 246, 0.7) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.25) !important;
}

.eval-title {
    font-size: 10px !important;
    font-weight: 700 !important;
    color: #a5b4fc !important;
    margin-bottom: 6px !important;
    text-transform: uppercase;
}

.eval-score {
    font-size: 18px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

/* ==================== SCROLLBAR ==================== */

::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(59, 130, 246, 0.05);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #3b82f6, #8b5cf6);
    border-radius: 10px;
    transition: all 0.3s;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #8b5cf6, #06b6d4);
}

/* ==================== TEXT & LAYOUT ==================== */

h1 { font-size: 26px !important; font-weight: 800 !important; }
h2 { font-size: 18px !important; font-weight: 700 !important; }
h3 { font-size: 14px !important; font-weight: 700 !important; }
p { font-size: 13px !important; }

.main-content {
    max-width: 1200px;
    margin: auto;
    padding: 20px;
    animation: fadeIn 0.6s ease-out;
}

hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent);
    margin: 20px 0 !important;
}

</style>
""", unsafe_allow_html=True)

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
                                             ["report", "article", "summary", "presentation"],
                                             label_visibility="collapsed")
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
                d1.download_button("📥 Markdown", data=content, file_name="research.md", use_container_width=True)
                d2.download_button(
                    "📥 JSON",
                    data=json.dumps(results, indent=2),
                    file_name="research.json",
                    use_container_width=True
                )
                d3.download_button("📥 TXT", data=content, file_name="research.txt", use_container_width=True)

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
                                    f"<p style='font-size:0.85rem; color:#a5b4fc; margin-top:4px;'>"
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
<p style='color:#a5b4fc; font-size:0.9rem;'>
{explanations['overall']}
</p>
""",
                            unsafe_allow_html=True,
                        )

                    except Exception as e:
                        st.warning(f"Evaluation unavailable: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error during research: {str(e)}")

# Tab 2 - Find Related
with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 🔗 Find Related Research")
    search_query = st.text_input("Search related topics", placeholder="Enter a topic...", label_visibility="collapsed")
    if search_query:
        st.info("Related research feature coming soon...")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3 - Past Sessions
with tab3:
    st.markdown("### 📂 Past Research Sessions")
    output_dir = Path("outputs")
    
    if output_dir.exists():
        json_files = list(output_dir.glob("*.json"))
        if json_files:
            for file in sorted(json_files, key=os.path.getmtime, reverse=True):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{data.get('query', 'Untitled')}**")
                    with col2:
                        if st.button("📖 View", key=f"view_{file.stem}", use_container_width=True):
                            st.json(data)
                except:
                    pass
        else:
            st.info("No past sessions found")
    else:
        st.info("No sessions directory yet")

# Sidebar - Stats and Recent
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

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; opacity:0.7; padding:14px; font-size:12px; color:#a5b4fc;'>
    AI Research Assistant v2.0 • Multi-Agent System<br>
    Powered by Claude & Tavily
</div>
""", unsafe_allow_html=True)
