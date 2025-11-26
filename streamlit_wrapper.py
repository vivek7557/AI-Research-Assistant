"""
Streamlit Web Interface for AI Research Assistant
Modern Web App Design - Clean, Centered Layout
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
    page_title="ResearchAI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# MODERN WEB APP UI CSS
st.markdown("""
<style>

/* ==================== ANIMATIONS ==================== */
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes shimmer { 0% { background-position: -1000px 0; } 100% { background-position: 1000px 0; } }

/* ==================== GLOBAL ==================== */
* { margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f47 50%, #0f1a35 100%) !important;
    min-height: 100vh;
}

[data-testid="stSidebar"] { display: none !important; }

[data-testid="stMain"] { padding: 0 !important; }

/* ==================== HEADER NAVBAR ==================== */
[data-testid="stHeader"] {
    background: linear-gradient(180deg, rgba(10, 14, 39, 0.95) 0%, rgba(26, 31, 71, 0.8) 100%) !important;
    border-bottom: 1px solid rgba(59, 130, 246, 0.2) !important;
    padding: 16px 0 !important;
    backdrop-filter: blur(10px) !important;
    position: sticky;
    top: 0;
    z-index: 100;
}

/* ==================== CONTAINER ==================== */
.main-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
    animation: fadeIn 0.6s ease-out;
}

/* ==================== CENTER TITLE ==================== */
.center-header {
    text-align: center;
    margin-bottom: 50px;
    animation: slideInUp 0.6s ease-out;
}

.center-header h1 {
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
}

.center-header p {
    font-size: 16px;
    color: #a5b4fc;
}

/* ==================== CENTERED CONTENT AREA ==================== */
.content-wrapper {
    display: flex;
    gap: 30px;
    margin-bottom: 40px;
    animation: slideInUp 0.7s ease-out;
}

.stats-panel {
    flex: 0 0 300px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.search-panel {
    flex: 1;
    min-width: 0;
}

/* ==================== STATS CARDS ==================== */
.stat-card {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%);
    border: 1px solid rgba(59, 130, 246, 0.35);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.12);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    animation: fadeIn 0.6s ease-out backwards;
}

.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.2s; }
.stat-card:nth-child(3) { animation-delay: 0.3s; }
.stat-card:nth-child(4) { animation-delay: 0.4s; }

.stat-card:hover {
    border-color: rgba(59, 130, 246, 0.6);
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.25);
}

.stat-label {
    font-size: 12px;
    font-weight: 700;
    color: #a5b4fc;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}

.stat-value {
    font-size: 32px;
    font-weight: 900;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ==================== SEARCH CARD ==================== */
.search-card {
    background: linear-gradient(135deg, rgba(22, 33, 62, 0.6) 0%, rgba(15, 52, 96, 0.6) 100%);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 16px;
    padding: 30px;
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.12);
    backdrop-filter: blur(10px);
    animation: slideInUp 0.6s ease-out;
}

.search-card:hover {
    border-color: rgba(59, 130, 246, 0.5);
    box-shadow: 0 12px 48px rgba(59, 130, 246, 0.2);
}

/* ==================== INPUTS ==================== */
input, select {
    background: rgba(15, 52, 96, 0.4) !important;
    border: 1.5px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    transition: all 0.3s !important;
}

input::placeholder { color: rgba(203, 213, 225, 0.5) !important; }

input:focus, select:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15) !important;
    background: rgba(15, 52, 96, 0.6) !important;
    outline: none !important;
}

/* ==================== BUTTONS ==================== */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%) !important;
    border: 1px solid rgba(59, 130, 246, 0.5) !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 12px 28px !important;
    height: 44px !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.35) !important;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.6) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border: 1px solid rgba(16, 185, 129, 0.5) !important;
    height: 44px !important;
    padding: 12px 28px !important;
    font-size: 13px !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 20px rgba(16, 185, 129, 0.35) !important;
    width: 100% !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(16, 185, 129, 0.6) !important;
}

/* ==================== TABS ==================== */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px !important;
    border-bottom: 1px solid rgba(59, 130, 246, 0.2) !important;
    padding-bottom: 14px !important;
    justify-content: center !important;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(59, 130, 246, 0.08) !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #cbd5e1 !important;
    transition: all 0.3s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    border-color: rgba(59, 130, 246, 0.6) !important;
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
}

[data-testid="stMetric"]:hover {
    border-color: rgba(59, 130, 246, 0.5) !important;
    transform: translateY(-4px) !important;
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

/* ==================== CONTENT ==================== */
.content-card {
    background: linear-gradient(135deg, rgba(22, 33, 62, 0.6) 0%, rgba(15, 52, 96, 0.6) 100%);
    border: 1px solid rgba(59, 130, 246, 0.3);
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.12);
    backdrop-filter: blur(10px);
    margin: 20px 0;
}

/* ==================== ALERTS ==================== */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-size: 13px !important;
    border-left: 4px solid !important;
    padding: 14px 16px !important;
    backdrop-filter: blur(10px) !important;
}

/* ==================== EXPANDER ==================== */
[data-testid="stExpander"] {
    border-radius: 10px !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.05)) !important;
}

/* ==================== TEXT ==================== */
h1 { font-size: 26px !important; font-weight: 800 !important; }
h2 { font-size: 18px !important; font-weight: 700 !important; }
h3 { font-size: 14px !important; font-weight: 700 !important; }
p { font-size: 13px !important; }

/* ==================== FOOTER ==================== */
.footer {
    text-align: center;
    padding: 30px 20px;
    color: #a5b4fc;
    font-size: 12px;
    margin-top: 40px;
}

/* ==================== SCROLLBAR ==================== */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(59, 130, 246, 0.05);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #3b82f6, #8b5cf6);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #8b5cf6, #06b6d4);
}

/* ==================== DIVIDER ==================== */
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

# Main wrapper
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# Center Title
st.markdown("""
<div class="center-header">
    <h1>🔍 ResearchAI</h1>
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

    # Stats and Search Side by Side
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    
    # Right - Search (Full Width)
    col1, col2 = st.columns([1, 1])
    
    with col2:
        st.markdown('<div class="search-card">', unsafe_allow_html=True)

        query = st.text_input(
            "Research Query",
            placeholder="e.g., Impact of artificial intelligence on healthcare",
            label_visibility="collapsed"
        )

        col_format, col_depth = st.columns(2)
        output_format = col_format.selectbox("📄 Format", ["report", "article", "summary", "presentation"], label_visibility="collapsed")
        run_evaluation = col_depth.checkbox("🎯 Evaluate", value=True)

        with st.expander("⚙️ Advanced"):
            colA, colB = st.columns(2)
            session_id_input = colA.text_input("Session ID", placeholder="research_xxxx")
            depth_level = colB.slider("Depth", 1, 5, 3)

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

                st.success("✅ Research completed!")

                st.markdown("---")
                st.markdown("### 📊 Metrics")

                final_content = results.get("final_content", {})
                summary = results.get("research_summary", {})
                validation = results.get("validation", {})

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("📚 Sources", summary.get("total_sources", 0))
                col2.metric("🔄 Iterations", summary.get("iterations", 0))
                col3.metric("🎯 Confidence", f"{validation.get('confidence_score', 0)}%")
                col4.metric("📝 Format", output_format.title())

                st.markdown("---")
                st.markdown("### 📄 Research")

                content = final_content.get("content", "")
                st.markdown(content)

                st.markdown("---")
                d1, d2, d3 = st.columns(3)
                d1.download_button("📥 MD", data=content, file_name="research.md", use_container_width=True)
                d2.download_button("📥 JSON", data=json.dumps(results, indent=2), file_name="research.json", use_container_width=True)
                d3.download_button("📥 TXT", data=content, file_name="research.txt", use_container_width=True)

                # Evaluation
                if run_evaluation:
                    st.markdown("---")
                    st.markdown("### 📊 Evaluation")

                    try:
                        evaluator = ResearchEvaluator()
                        metrics = evaluator.evaluate_research(query, results)
                        metrics_dict = metrics.to_dict()

                        explanations = {
                            "completeness": "How fully the research covers all aspects",
                            "accuracy": "Factual correctness based on sources",
                            "relevance": "How closely content matches query",
                            "quality": "Structure, clarity, and flow",
                            "efficiency": "Quality of sources and conciseness",
                            "citations": "Source referencing quality",
                            "overall": "Weighted average of all metrics",
                        }

                        for metric, score in metrics_dict.items():
                            m_name = metric.replace("_", " ").title()
                            left, right = st.columns([3, 1])
                            with left:
                                st.markdown(f"**{m_name}**")
                                st.progress(score / 100)
                                st.caption(explanations.get(metric, ''))
                            with right:
                                st.metric("", f"{score:.0f}", delta=None)

                        st.markdown("---")
                        overall = metrics.overall_score
                        emoji = "🟢" if overall >= 80 else "🟡" if overall >= 60 else "🔴"
                        st.markdown(f"### {emoji} Quality: {overall:.1f}/100")

                    except Exception as e:
                        st.warning("Evaluation unavailable")
            except Exception as e:
                st.error(f"Error: {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 🔗 Find Related Research")
    search_query = st.text_input("Search topics", placeholder="Enter a topic...", label_visibility="collapsed")
    if search_query:
        st.info("Coming soon...")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3
with tab3:
    st.markdown("### 📂 Past Sessions")
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
                        if st.button("View", key=f"view_{file.stem}", use_container_width=True):
                            st.json(data)
                except:
                    pass

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    ResearchAI v2.0 • Powered by Claude & Tavily
</div>
""", unsafe_allow_html=True)
