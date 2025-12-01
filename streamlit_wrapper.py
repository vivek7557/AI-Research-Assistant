"""
Streamlit Web Interface for AI Research Assistant
Fresh Modern UI - Clean & Minimalist Design
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

st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
    initial_sidebar_collapsed=True
)

# Fresh Modern CSS - Minimalist Design
st.markdown("""
<style>
    /* Reset Everything */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Variables */
    :root {
        --primary: #2563eb;
        --secondary: #7c3aed;
        --accent: #06b6d4;
        --success: #059669;
        --bg: #ffffff;
        --bg-light: #f8fafc;
        --border: #e2e8f0;
        --text: #0f172a;
        --text-light: #475569;
    }
    
    /* Animations */
    @keyframes fadeIn { 
        from { opacity: 0; } 
        to { opacity: 1; } 
    }
    
    @keyframes slideUp { 
        from { opacity: 0; transform: translateY(20px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    
    /* Override Streamlit */
    .appViewContainer {
        background: #ffffff !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #ffffff !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] {
        display: none !important;
        width: 0 !important;
    }
    
    .main {
        background: #ffffff !important;
        padding: 0 !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Hide sidebar toggle */
    button[data-testid="baseButton-secondary"] {
        display: none !important;
    }
    
    /* Header Navigation */
    .header-nav {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-bottom: 1px solid var(--border);
        padding: 1.5rem 2rem;
        position: sticky;
        top: 0;
        z-index: 100;
        width: 100vw;
        margin-left: calc(-50vw + 50%);
    }
    
    .nav-container {
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .nav-logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--text);
    }
    
    .nav-logo-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .nav-stats {
        display: flex;
        gap: 2rem;
    }
    
    .nav-stat {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.25rem;
    }
    
    .nav-stat-value {
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .nav-stat-label {
        font-size: 0.75rem;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Main Content */
    .main-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 3rem 2rem;
        background: #ffffff;
    }
    
    /* Hero Section */
    .hero {
        text-align: center;
        margin-bottom: 3rem;
        animation: slideUp 0.6s ease;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: var(--text);
        margin-bottom: 0.75rem;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-light);
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    .hero-description {
        font-size: 1rem;
        color: var(--text-light);
        max-width: 600px;
        margin: 0 auto 2rem;
        line-height: 1.6;
    }
    
    /* Search Card */
    .search-card {
        background: var(--bg-light);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 3rem;
        animation: slideUp 0.7s ease;
    }
    
    /* Inputs */
    .stTextInput > label,
    .stSelectbox > label,
    .stSlider > label {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: var(--text) !important;
        margin-bottom: 0.75rem !important;
    }
    
    .stTextInput input {
        background: #ffffff !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        padding: 0.875rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary) !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    .stSelectbox select {
        background: #ffffff !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        padding: 0.875rem 1rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2) !important;
        height: auto !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3) !important;
    }
    
    .stDownloadButton > button {
        background: var(--bg-light) !important;
        border: 2px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.875rem 1.75rem !important;
        transition: all 0.3s ease !important;
        height: auto !important;
    }
    
    .stDownloadButton > button:hover {
        border-color: var(--primary) !important;
        background: #ffffff !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-light) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        font-weight: 600 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem !important;
        justify-content: center !important;
        border-bottom: 2px solid var(--border) !important;
        padding: 0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        color: var(--text-light) !important;
        font-weight: 600 !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom-color: var(--primary) !important;
        background: transparent !important;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: var(--bg-light);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* Progress */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        border-radius: 10px !important;
    }
    
    /* Section */
    .section {
        background: var(--bg-light);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        animation: slideUp 0.6s ease;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--border);
    }
    
    /* Footer */
    .footer {
        background: var(--bg-light);
        border-top: 1px solid var(--border);
        padding: 2rem;
        text-align: center;
        color: var(--text-light);
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title { font-size: 2rem; }
        .main-content { padding: 1.5rem 1rem; }
        .search-card { padding: 1.5rem; }
        .nav-stats { gap: 1rem; }
    }
</style>
""", unsafe_allow_html=True)
    
    /* Header Navigation */
    .header-nav {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-bottom: 1px solid var(--border);
        padding: 1.5rem 2rem;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .nav-logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--text);
    }
    
    .nav-logo-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .nav-stats {
        display: flex;
        gap: 2rem;
    }
    
    .nav-stat {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.25rem;
    }
    
    .nav-stat-value {
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .nav-stat-label {
        font-size: 0.75rem;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Main Content */
    .main-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 3rem 2rem;
    }
    
    /* Hero Section */
    .hero {
        text-align: center;
        margin-bottom: 3rem;
        animation: slideUp 0.6s ease;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: var(--text);
        margin-bottom: 0.75rem;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-light);
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    .hero-description {
        font-size: 1rem;
        color: var(--text-light);
        max-width: 600px;
        margin: 0 auto 2rem;
        line-height: 1.6;
    }
    
    /* Search Card */
    .search-card {
        background: var(--bg-light);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 3rem;
        animation: slideUp 0.7s ease;
    }
    
    /* Inputs */
    .stTextInput > label,
    .stSelectbox > label,
    .stSlider > label {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: var(--text) !important;
        margin-bottom: 0.75rem !important;
    }
    
    .stTextInput input {
        background: #ffffff !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        padding: 0.875rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary) !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    .stSelectbox select {
        background: #ffffff !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        padding: 0.875rem 1rem !important;
    }
    
    .stSlider > div > div {
        background: var(--border) !important;
    }
    
    /* Columns */
    .stColumns > div {
        gap: 1.5rem !important;
    }
    
    /* Checkboxes */
    .stCheckbox {
        color: var(--text) !important;
    }
    
    .stCheckbox > label {
        font-weight: 500 !important;
        color: var(--text) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2) !important;
        height: auto !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    .stDownloadButton > button {
        background: var(--bg-light) !important;
        border: 2px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.875rem 1.75rem !important;
        transition: all 0.3s ease !important;
        height: auto !important;
    }
    
    .stDownloadButton > button:hover {
        border-color: var(--primary) !important;
        background: #ffffff !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-light) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        font-weight: 600 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem !important;
        justify-content: center !important;
        border-bottom: 2px solid var(--border) !important;
        padding: 0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        color: var(--text-light) !important;
        font-weight: 600 !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text) !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom-color: var(--primary) !important;
        background: transparent !important;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: var(--bg-light);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-light) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }
    
    /* Progress */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        border-radius: 10px !important;
    }
    
    /* Section */
    .section {
        background: var(--bg-light);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        animation: slideUp 0.6s ease;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--border);
    }
    
    /* Alert */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        border-top: 1px solid var(--border) !important;
        margin: 2rem 0 !important;
    }
    
    /* Markdown */
    .markdown-text-container {
        color: var(--text);
        line-height: 1.8;
    }
    
    /* Footer */
    .footer {
        background: var(--bg-light);
        border-top: 1px solid var(--border);
        padding: 2rem;
        text-align: center;
        color: var(--text-light);
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title { font-size: 2rem; }
        .main-content { padding: 1.5rem 1rem; }
        .search-card { padding: 1.5rem; }
        .nav-stats { gap: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# Header Navigation
anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "")

if anthropic_key:
    os.environ["ANTHROPIC_API_KEY"] = anthropic_key
if tavily_key:
    os.environ["TAVILY_API_KEY"] = tavily_key

keys_set = bool(anthropic_key and tavily_key)

try:
    memory_bank = MemoryBank()
    stats = memory_bank.get_statistics()
except:
    stats = {"total_memories": 0, "completed_sessions": 0, "total_sources": 0}

st.markdown(f"""
<div class="header-nav">
    <div class="nav-container">
        <div class="nav-logo">
            <div class="nav-logo-icon">🔍</div>
            <span>ResearchAI</span>
        </div>
        <div class="nav-stats">
            <div class="nav-stat">
                <div class="nav-stat-value">{stats.get('total_memories', 0)}</div>
                <div class="nav-stat-label">Research</div>
            </div>
            <div class="nav-stat">
                <div class="nav-stat-value">{stats.get('completed_sessions', 0)}</div>
                <div class="nav-stat-label">Completed</div>
            </div>
            <div class="nav-stat">
                <div class="nav-stat-value">{stats.get('total_sources', 0)}</div>
                <div class="nav-stat-label">Sources</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1 class="hero-title">Deep Research</h1>
    <p class="hero-subtitle">Powered by AI Agents</p>
    <p class="hero-description">
        Conduct comprehensive research on any topic with multi-agent AI collaboration, 
        quality evaluation, and multiple output formats.
    </p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔬 Research", "🔍 Related", "📂 History"])

# Tab 1
with tab1:
    if not keys_set:
        st.error("⚠️ Missing API Keys - Configure ANTHROPIC_API_KEY and TAVILY_API_KEY")
        st.stop()
    
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    
    st.markdown("<h3 style='margin-top:0;color:#0f172a;'>Start Your Research</h3>", unsafe_allow_html=True)
    
    query = st.text_input(
        "What do you want to research?",
        placeholder="e.g., Impact of AI on healthcare",
        label_visibility="visible"
    )
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        output_format = st.selectbox(
            "Output Format",
            ["report", "article", "summary", "presentation"],
            label_visibility="visible"
        )
    
    with col2:
        run_evaluation = st.checkbox("Run Evaluation", value=True)
    
    with st.expander("⚙️ Advanced Settings"):
        col_adv1, col_adv2 = st.columns(2)
        with col_adv1:
            session_id_input = st.text_input("Session ID", placeholder="Optional")
        with col_adv2:
            depth_level = st.slider("Research Depth", 1, 5, 3)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Start Research", use_container_width=True):
        if not query:
            st.warning("Please enter a research query")
            st.stop()
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.info("🎯 Initializing research agents...")
            progress_bar.progress(20)
            orchestrator = ResearchOrchestrator()
            
            status_text.info("📋 Planning research strategy...")
            progress_bar.progress(40)
            
            status_text.info("🔍 Conducting deep research...")
            progress_bar.progress(60)
            
            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None
            )
            
            status_text.info("✅ Finalizing report...")
            progress_bar.progress(100)
            
            progress_bar.empty()
            status_text.empty()
            
            st.success("✅ Research completed!")
            
            # Metrics
            st.markdown("---")
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Research Metrics</h2>', unsafe_allow_html=True)
            
            final_content = results.get("final_content", {})
            summary = results.get("research_summary", {})
            validation = results.get("validation", {})
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("📚 Sources", summary.get("total_sources", 0))
            m2.metric("🔄 Iterations", summary.get("iterations", 0))
            m3.metric("🎯 Confidence", f"{validation.get('confidence_score', 0)}%")
            m4.metric("📝 Format", output_format.title())
            
            st.markdown('</div>', unsafe_after_html=True)
            
            # Content
            st.markdown("---")
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Generated Research</h2>', unsafe_allow_html=True)
            
            content = final_content.get("content", "")
            if not content:
                st.warning(f"⚠️ No {output_format} content generated")
            else:
                st.markdown(content)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Downloads
            st.markdown("---")
            st.markdown('<div class="section">', unsafe_allow_html=True)
            d1, d2, d3 = st.columns(3)
            d1.download_button("📥 Markdown", content, "research.md", use_container_width=True)
            d2.download_button("📥 JSON", json.dumps(results, indent=2), "research.json", use_container_width=True)
            d3.download_button("📥 TXT", content, "research.txt", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Evaluation
            if run_evaluation:
                st.markdown("---")
                st.markdown('<div class="section">', unsafe_allow_html=True)
                st.markdown('<h2 class="section-title">Quality Evaluation</h2>', unsafe_allow_html=True)
                
                try:
                    evaluator = ResearchEvaluator()
                    metrics = evaluator.evaluate_research(query, results)
                    metrics_dict = metrics.to_dict()
                    
                    for metric, score in list(metrics_dict.items())[:6]:
                        m_name = metric.replace("_", " ").title()
                        col_eval1, col_eval2 = st.columns([3, 1])
                        with col_eval1:
                            st.write(f"**{m_name}**")
                            st.progress(score / 100)
                        with col_eval2:
                            st.metric("", f"{score:.0f}", delta=None)
                    
                    st.markdown("---")
                    overall = metrics.overall_score
                    emoji = "🟢" if overall >= 80 else "🟡" if overall >= 60 else "🔴"
                    st.markdown(f"## {emoji} Quality Score: {overall:.1f}/100")
                
                except Exception as e:
                    st.warning(f"Evaluation unavailable: {str(e)}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Tab 2
with tab2:
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>Find Related Research</h3>", unsafe_allow_html=True)
    
    related_query = st.text_input(
        "Search keywords",
        placeholder="Enter topic to find related research",
        label_visibility="visible"
    )
    
    if st.button("🔎 Search", use_container_width=True):
        if related_query:
            try:
                memory_bank = MemoryBank()
                related = memory_bank.get_related_research(related_query, limit=10)
                
                if related:
                    st.success(f"✅ Found {len(related)} related sessions")
                    for session in related:
                        with st.expander(f"📄 {session.get('query', 'Untitled')}"):
                            st.write(f"**Sources:** {session.get('sources_count', 0)}")
                else:
                    st.info("No related research found")
            except Exception as e:
                st.error(f"Search failed: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3
with tab3:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Past Research Sessions</h2>', unsafe_allow_html=True)
    
    output_dir = Path("outputs")
    if output_dir.exists():
        json_files = list(output_dir.glob("*.json"))
        
        if json_files:
            st.info(f"📊 {len(json_files)} sessions found")
            
            for json_file in sorted(json_files, key=os.path.getmtime, reverse=True)[:20]:
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                    
                    with st.expander(f"📄 {data.get('query', 'Untitled')}"):
                        c1, c2 = st.columns(2)
                        c1.write(f"**ID:** {data.get('session_id', 'N/A')[:12]}...")
                        c2.write(f"**Format:** {data.get('output_format', 'N/A')}")
                        
                        summary = data.get('research_summary', {})
                        c1.write(f"**Sources:** {summary.get('total_sources', 0)}")
                        c2.write(f"**Iterations:** {summary.get('iterations', 0)}")
                        
                        st.download_button(
                            "📥 Download",
                            json.dumps(data, indent=2),
                            json_file.name,
                            use_container_width=True
                        )
                except:
                    pass
        else:
            st.info("📭 No sessions yet")
    else:
        st.info("📭 No history")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <strong>ResearchAI v2.0</strong> • Multi-Agent System • Built with Streamlit
</div>
""", unsafe_allow_html=True)
