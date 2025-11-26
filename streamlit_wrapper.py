"""
Streamlit Web Interface for AI Research Assistant
Modern UI with centered layout and comprehensive analysis
Enhanced with modern animations, gradients, and premium styling
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

# Enhanced Custom CSS for modern UI
ENHANCED_CSS = """
<style>

/* COLOR PALETTE */
:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --secondary: #8b5cf6;
    --accent: #ec4899;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --bg-dark: #0f172a;
    --bg-card: #1e293b;
    --bg-input: #0f172a;
    --border: #334155;
    --text-primary: #f1f5f9;
    --text-secondary: #cbd5e1;
}

/* ANIMATIONS */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes shimmer {
    from { background-position: -1000px 0; }
    to { background-position: 1000px 0; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* GLOBAL THEME */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1a1f35 100%);
}

[data-testid="stSidebarContent"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}

.main-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
    animation: fadeInUp 0.7s ease-out;
}

/* HEADER STYLING */
.main-header {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
    border: 2px solid rgba(99, 102, 241, 0.3);
    border-radius: 20px;
    padding: 3rem 2rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
    animation: fadeInUp 0.8s ease-out;
}

.main-header h1 {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 4s ease infinite;
    margin: 0;
}

.main-header p {
    font-size: 1.1rem;
    color: #cbd5e1;
    margin-top: 0.5rem;
}

/* INPUT CONTAINER */
.input-container {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
    border: 2px solid rgba(99, 102, 241, 0.3);
    border-radius: 18px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    animation: slideInLeft 0.8s ease-out;
    transition: all 0.3s ease;
}

.input-container:hover {
    border-color: rgba(99, 102, 241, 0.6);
    box-shadow: 0 12px 48px rgba(99, 102, 241, 0.2);
    transform: translateY(-2px);
}

/* TEXT INPUT */
[data-testid="stTextInput"] input {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 2px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    padding: 12px 16px !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    background: rgba(15, 23, 42, 0.9) !important;
}

/* SELECTBOX */
[data-testid="stSelectbox"] {
    animation: slideInRight 0.8s ease-out 0.1s both;
}

[data-baseweb="select"] {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 2px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 12px !important;
}

/* CHECKBOX */
[data-testid="stCheckbox"] {
    animation: slideInRight 0.8s ease-out 0.15s both;
}

[role="checkbox"] {
    accent-color: #6366f1 !important;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border: none;
    color: white !important;
    font-weight: 700 !important;
    padding: 14px 32px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3) !important;
    font-size: 1.05rem !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 32px rgba(99, 102, 241, 0.5) !important;
}

.stButton > button:active {
    transform: translateY(-1px) !important;
}

/* DOWNLOAD BUTTON */
.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(16, 185, 129, 0.5) !important;
}

/* PROGRESS BAR */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%) !important;
    background-size: 200% 100%;
    animation: shimmer 2s infinite;
}

.stProgress > div > div {
    animation: pulse 2s ease-in-out infinite;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 1rem;
    border-bottom: 2px solid rgba(99, 102, 241, 0.2);
    animation: slideInRight 0.8s ease-out 0.2s both;
}

.stTabs [data-baseweb="tab"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05)) !important;
    border: 2px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    color: #cbd5e1 !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    border-color: #6366f1 !important;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.15)) !important;
    transform: translateY(-2px);
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    border-color: #6366f1 !important;
    color: white !important;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
}

/* EXPANDER */
[data-testid="stExpander"] {
    border: 2px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 12px !important;
    animation: scaleIn 0.5s ease-out;
}

[data-testid="stExpander"] > div > button {
    background: rgba(99, 102, 241, 0.05) !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stExpander"] > div > button:hover {
    background: rgba(99, 102, 241, 0.1) !important;
}

/* METRICS */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(139, 92, 246, 0.08));
    border: 2px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    animation: scaleIn 0.6s ease-out;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #6366f1;
    box-shadow: 0 12px 32px rgba(99, 102, 241, 0.25);
}

[data-testid="stMetric"] label {
    color: #cbd5e1 !important;
    font-weight: 600;
}

[data-testid="stMetric"] div {
    color: #6366f1 !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
}

/* CONTENT CARDS */
.content-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8));
    border: 2px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    animation: fadeInUp 0.8s ease-out;
    transition: all 0.3s ease;
}

.content-card:hover {
    border-color: #6366f1;
    box-shadow: 0 12px 32px rgba(99, 102, 241, 0.25);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 2px solid rgba(99, 102, 241, 0.2);
}

.sidebar-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
    border: 2px solid rgba(99, 102, 241, 0.3);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    animation: slideInLeft 0.6s ease-out;
}

.sidebar-card:hover {
    transform: translateX(6px);
    border-color: #6366f1;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
}

.sidebar-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #cbd5e1;
    margin-bottom: 0.5rem;
}

.sidebar-value {
    font-size: 1.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sidebar-activity-title {
    margin-top: 1.5rem;
    font-size: 1rem;
    font-weight: 700;
    color: #f1f5f9;
    padding-bottom: 0.8rem;
    border-bottom: 2px solid rgba(99, 102, 241, 0.3);
}

.sidebar-activity-item {
    font-size: 0.85rem;
    color: #cbd5e1;
    padding: 0.6rem;
    margin-bottom: 0.4rem;
    border-left: 3px solid rgba(99, 102, 241, 0.4);
    padding-left: 1rem;
    transition: all 0.2s ease;
    border-radius: 4px;
}

.sidebar-activity-item:hover {
    color: #6366f1;
    border-left-color: #6366f1;
    background: rgba(99, 102, 241, 0.05);
    padding-left: 1.2rem;
}

/* EVALUATION SECTION */
.eval-right {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
    border: 2px solid rgba(99, 102, 241, 0.4);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    animation: slideInRight 0.6s ease-out;
    transition: all 0.3s ease;
}

.eval-right:hover {
    border-color: #6366f1;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
    transform: translateY(-2px);
}

.eval-title {
    font-size: 0.75rem;
    color: #cbd5e1;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.eval-score {
    font-size: 1.6rem;
    font-weight: 900;
    color: #6366f1;
}

/* ALERTS */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 2px solid !important;
    backdrop-filter: blur(10px);
    animation: slideInLeft 0.5s ease-out;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(99, 102, 241, 0.05);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #6366f1, #8b5cf6);
    border-radius: 10px;
    transition: all 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #8b5cf6, #ec4899);
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 1.8rem;
    }
    .main-content {
        padding: 1rem;
    }
}

</style>
"""

st.markdown(ENHANCED_CSS, unsafe_allow_html=True)

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
                                    f"<p style='font-size:0.85rem; color:#cbd5e1; margin-top:4px;'>"
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
<p style='color:#cbd5e1; font-size:0.9rem;'>
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
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown("### 🔗 Find Related Research")
    search_query = st.text_input("Search related topics", placeholder="Enter a topic...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if search_query:
        st.info("Related research feature coming soon...")


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
                        if st.button("📖 View", key=f"view_{file.stem}"):
                            st.json(data)
                except:
                    pass
        else:
            st.info("No past sessions found")
    else:
        st.info("No sessions directory yet")


st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; opacity:0.7; padding:1rem; color:#cbd5e1;'>
    AI Research Assistant v2.0 • Multi-Agent System<br>
    Powered by Claude & Tavily
</div>
""", unsafe_allow_html=True)
