"""
Streamlit Web Interface for AI Research Assistant
Modern Gradient UI with animations
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

# Custom CSS with Modern Gradients
st.markdown("""
<style>
/* ====================================== */
/*         ANIMATED BACKGROUND            */
/* ====================================== */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    background-attachment: fixed;
}

/* Floating gradient orbs */
@keyframes float {
    0%, 100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-20px) scale(1.05); }
}

.main::before {
    content: '';
    position: fixed;
    top: 10%;
    left: 10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(147,51,234,0.3) 0%, transparent 70%);
    border-radius: 50%;
    filter: blur(80px);
    animation: float 8s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

.main::after {
    content: '';
    position: fixed;
    bottom: 10%;
    right: 10%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(59,130,246,0.3) 0%, transparent 70%);
    border-radius: 50%;
    filter: blur(90px);
    animation: float 10s ease-in-out infinite reverse;
    pointer-events: none;
    z-index: 0;
}

/* ====================================== */
/*         PREMIUM ANIMATIONS             */
/* ====================================== */
@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(147,51,234,0.5); }
    50% { box-shadow: 0 0 40px rgba(147,51,234,0.8); }
}

.fade-in {
    animation: fadeInUp 0.8s ease both;
}

/* ====================================== */
/*         HEADER WITH GRADIENT           */
/* ====================================== */
.main-header {
    background: linear-gradient(135deg, rgba(147,51,234,0.1) 0%, rgba(59,130,246,0.1) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 3rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    animation: fadeInUp 0.8s ease;
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #9333ea, #3b82f6, #ec4899, #9333ea);
    border-radius: 24px;
    opacity: 0.5;
    filter: blur(20px);
    z-index: -1;
    animation: shimmer 3s linear infinite;
    background-size: 400% 400%;
}

.main-header h1 {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #a78bfa 0%, #ec4899 50%, #60a5fa 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 8s ease infinite;
    margin: 0;
}

.main-header p {
    font-size: 1.2rem;
    color: rgba(255,255,255,0.7);
    margin-top: 0.5rem;
}

/* ====================================== */
/*         GLASS MORPHISM CARDS           */
/* ====================================== */
.glass-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: all 0.4s ease;
    animation: fadeInUp 1s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 48px rgba(147,51,234,0.4);
    border-color: rgba(147,51,234,0.5);
}

/* ====================================== */
/*         GRADIENT BUTTONS               */
/* ====================================== */
.stButton > button {
    background: linear-gradient(135deg, #9333ea 0%, #ec4899 100%);
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 16px;
    font-weight: 700;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(147,51,234,0.5);
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 40px rgba(147,51,234,0.8);
    animation: glow 1.5s ease-in-out infinite;
}

/* ====================================== */
/*         METRIC CARDS                   */
/* ====================================== */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(147,51,234,0.15) 0%, rgba(59,130,246,0.15) 100%);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border-color: rgba(147,51,234,0.5);
}

[data-testid="stMetric"] label {
    color: rgba(255,255,255,0.8) !important;
    font-size: 0.9rem !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: white !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

/* ====================================== */
/*         INPUT FIELDS                   */
/* ====================================== */
.stTextInput > div > div {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    transition: all 0.3s ease;
}

.stTextInput > div > div:hover {
    border-color: rgba(147,51,234,0.5);
    box-shadow: 0 0 20px rgba(147,51,234,0.3);
}

.stTextInput input {
    color: white !important;
    font-size: 1.1rem;
    padding: 1rem;
}

.stTextInput input::placeholder {
    color: rgba(255,255,255,0.4);
}

/* ====================================== */
/*         SELECT BOXES                   */
/* ====================================== */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    color: white;
}

/* ====================================== */
/*         TABS                           */
/* ====================================== */
.stTabs [data-baseweb="tab-list"] {
    gap: 1rem;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(10px);
    padding: 1rem 2rem !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: rgba(255,255,255,0.7) !important;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    transform: translateY(-2px);
    border-color: rgba(147,51,234,0.5) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(147,51,234,0.3) 0%, rgba(236,72,153,0.3) 100%) !important;
    border-color: rgba(147,51,234,0.7) !important;
    color: white !important;
    box-shadow: 0 4px 20px rgba(147,51,234,0.4);
}

/* ====================================== */
/*         PROGRESS BAR                   */
/* ====================================== */
.stProgress > div > div {
    background: linear-gradient(90deg, #9333ea, #ec4899, #3b82f6);
    background-size: 200% 100%;
    animation: shimmer 2s linear infinite;
}

/* ====================================== */
/*         SIDEBAR                        */
/* ====================================== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,12,41,0.95) 0%, rgba(36,36,62,0.95) 100%);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

.sidebar-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.sidebar-card:hover {
    transform: scale(1.03);
    border-color: rgba(147,51,234,0.5);
    box-shadow: 0 4px 20px rgba(147,51,234,0.3);
}

.sidebar-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: rgba(255,255,255,0.7);
    margin-bottom: 0.5rem;
}

.sidebar-value {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ====================================== */
/*         DOWNLOAD BUTTONS               */
/* ====================================== */
.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(147,51,234,0.2) 0%, rgba(59,130,246,0.2) 100%) !important;
    backdrop-filter: blur(10px);
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 12px;
    transition: all 0.3s ease;
}

.stDownloadButton > button:hover {
    transform: scale(1.05);
    border-color: rgba(147,51,234,0.6) !important;
    box-shadow: 0 4px 20px rgba(147,51,234,0.4);
}

/* ====================================== */
/*         MARKDOWN CONTENT               */
/* ====================================== */
.main .block-container {
    max-width: 1200px;
    padding: 2rem;
}

/* ====================================== */
/*         EXPANDER                       */
/* ====================================== */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    color: white !important;
}

/* ====================================== */
/*         SCROLLBAR                      */
/* ====================================== */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(0,0,0,0.2);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #9333ea, #ec4899);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #a855f7, #f472b6);
}

/* ====================================== */
/*         TEXT COLORS                    */
/* ====================================== */
.main h1, .main h2, .main h3 {
    color: white !important;
}

.main p, .main div, .main span {
    color: rgba(255,255,255,0.9) !important;
}

</style>
""", unsafe_allow_html=True)

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

# API Keys
anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "")

if anthropic_key:
    os.environ["ANTHROPIC_API_KEY"] = anthropic_key
if tavily_key:
    os.environ["TAVILY_API_KEY"] = tavily_key

keys_set = bool(anthropic_key and tavily_key)

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

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

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
            status_text.info("🎯 Initializing research system...")
            progress_bar.progress(20)
            orchestrator = ResearchOrchestrator()

            status_text.info("📋 Planning research strategy...")
            progress_bar.progress(40)

            status_text.info("🤖 Running AI agents...")
            progress_bar.progress(60)
            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None,
            )

            status_text.info("✨ Finalizing results...")
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

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            content = final_content.get("content", "")
            st.markdown(content)
            st.markdown('</div>', unsafe_allow_html=True)

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

                    for metric, score in metrics_dict.items():
                        m_name = metric.replace("_", " ").title()
                        st.markdown(f"**{m_name}**")
                        st.progress(score / 100)
                        st.write(f"Score: {score}/100")

                    st.markdown("---")
                    overall = metrics.overall_score
                    emoji = "🟢" if overall >= 80 else "🟡" if overall >= 60 else "🔴"
                    st.markdown(f"## {emoji} Overall Quality Score: {overall:.1f}/100")

                except Exception as e:
                    st.warning(f"Evaluation unavailable: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error during research: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; opacity:0.7; padding:1rem'>
    AI Research Assistant v2.0 • Multi-Agent System<br>
    Powered by Claude & Tavily
</div>
""", unsafe_allow_html=True)
