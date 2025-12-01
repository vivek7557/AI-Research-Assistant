"""
Streamlit Web Interface for AI Research Assistant
Beautiful Modern UI with Format Fix
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

# Beautiful Modern CSS
st.markdown("""
<style>
    :root {
        --primary: #3b82f6;
        --primary-dark: #2563eb;
        --secondary: #8b5cf6;
        --accent: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg: #0f172a;
        --bg-card: #1e293b;
        --border: #334155;
        --text: #f1f5f9;
        --text-secondary: #cbd5e1;
    }
    
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes slideInRight { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
    @keyframes shimmer { 0% { background-position: -1000px 0; } 100% { background-position: 1000px 0; } }
    
    .main { background: var(--bg); }
    
    .block-container { 
        padding: 2rem 3rem !important; 
        max-width: 1400px !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg) 0%, var(--bg-card) 100%);
        border-right: 1px solid var(--border);
    }
    
    .sidebar-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease;
    }
    
    .sidebar-card:hover {
        transform: translateY(-2px);
        border-color: var(--primary);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15);
    }
    
    .sidebar-title {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-value {
        font-size: 1.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sidebar-section-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: var(--text);
        margin: 1.5rem 0 0.75rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border);
    }
    
    .sidebar-activity-item {
        font-size: 0.8rem;
        color: var(--text-secondary);
        padding: 0.5rem 0;
        border-left: 2px solid transparent;
        padding-left: 0.5rem;
        margin-bottom: 0.25rem;
        transition: all 0.2s ease;
    }
    
    .sidebar-activity-item:hover {
        color: var(--text);
        border-left-color: var(--primary);
        padding-left: 0.75rem;
    }
    
    .hero-header {
        background: linear-gradient(135deg, var(--bg-card) 0%, #1a2847 100%);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        position: relative;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        font-weight: 500;
        position: relative;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        justify-content: center;
        background: transparent;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: var(--primary) !important;
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        border-color: var(--primary) !important;
        color: white !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }
    
    .input-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 900px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 0.7s ease;
        transition: all 0.3s ease;
    }
    
    .input-card:hover {
        border-color: var(--primary);
        box-shadow: 0 10px 40px rgba(59, 130, 246, 0.2);
    }
    
    .stTextInput input {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text) !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stSelectbox select {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text) !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.875rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stDownloadButton > button {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        border-color: var(--primary) !important;
        background: var(--bg-card) !important;
    }
    
    [data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: var(--primary);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15);
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        border-radius: 10px !important;
    }
    
    .content-section {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        animation: fadeInUp 0.6s ease;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid var(--border);
    }
    
    .eval-metric {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        animation: slideInRight 0.5s ease;
    }
    
    .eval-metric:hover {
        border-color: var(--primary);
        transform: translateX(5px);
    }
    
    .eval-name {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text);
    }
    
    .eval-score {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text) !important;
    }
    
    .stAlert { border-radius: 12px !important; }
    
    hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: var(--text-secondary);
        font-size: 0.875rem;
        border-top: 1px solid var(--border);
        margin-top: 3rem;
    }
    
    @media (max-width: 768px) {
        .hero-title { font-size: 2rem; }
        .block-container { padding: 1rem !important; }
        .input-card { padding: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-section-title">📊 Research Analytics</div>', unsafe_allow_html=True)

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
            <div class="sidebar-value">{stats.get('avg_importance', 0):.1f}<span style="font-size:1rem;color:var(--text-secondary);">/10</span></div>
        </div>
        """, unsafe_allow_html=True)
    except:
        st.info("📊 Statistics will appear after first research")

    st.markdown('<div class="sidebar-section-title">📈 Recent Activity</div>', unsafe_allow_html=True)

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
                    st.markdown(f'<div class="sidebar-activity-item">• {query[:32]}...</div>', unsafe_allow_html=True)
                except:
                    pass
        else:
            st.markdown('<div class="sidebar-activity-item">No recent activity</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-activity-item">No activity yet</div>', unsafe_allow_html=True)

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
<div class="hero-header">
    <div class="hero-title">🔍 AI Research Assistant</div>
    <div class="hero-subtitle">Deep research powered by multi-agent AI system</div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔬 New Research", "🔍 Find Related", "📂 Past Sessions"])

# Tab 1 - New Research
with tab1:
    if not keys_set:
        st.error("⚠️ API Keys missing. Please configure ANTHROPIC_API_KEY and TAVILY_API_KEY in .env file")
        st.stop()

    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    query = st.text_input(
        "🔎 Research Query",
        placeholder="e.g., Impact of artificial intelligence on healthcare systems",
        label_visibility="collapsed"
    )

    col_format, col_eval = st.columns([3, 2])
    with col_format:
        output_format = st.selectbox(
            "📄 Output Format",
            ["report", "article", "summary", "presentation"]
        )
    with col_eval:
        run_evaluation = st.checkbox("🎯 Run Evaluation", value=True)

    with st.expander("⚙️ Advanced Options"):
        colA, colB = st.columns(2)
        with colA:
            session_id_input = st.text_input("Resume Session ID", placeholder="research_xxxxx")
        with colB:
            depth_level = st.slider("Research Depth", 1, 5, 3)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 Start Research", use_container_width=True):
        if not query:
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
            
            # ✅ FIX: Pass output_format to orchestrator
            results = orchestrator.conduct_research(
                query=query,
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
            st.markdown('<div class="section-title">📊 Research Metrics</div>', unsafe_allow_html=True)

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
            st.markdown('<div class="section-title">📄 Generated Research</div>', unsafe_allow_html=True)

            content = final_content.get("content", "")
            if not content:
                st.warning(f"⚠️ No {output_format} content generated. This may be an orchestrator issue.")
                st.info("💡 Make sure your orchestrator.conduct_research() returns content for all formats.")
            else:
                st.markdown(content)

            # Downloads
            st.markdown("---")
            d1, d2, d3 = st.columns(3)
            d1.download_button("📥 Download Markdown", data=content, file_name="research.md", use_container_width=True)
            d2.download_button("📥 Download JSON", data=json.dumps(results, indent=2), file_name="research.json", use_container_width=True)
            d3.download_button("📥 Download TXT", data=content, file_name="research.txt", use_container_width=True)

            # Evaluation
            if run_evaluation:
                st.markdown("---")
                st.markdown('<div class="section-title">📊 Quality Evaluation</div>', unsafe_allow_html=True)

                try:
                    evaluator = ResearchEvaluator()
                    metrics = evaluator.evaluate_research(query, results)
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
                        
                        st.markdown(f"""
                        <div class="eval-metric">
                            <div class="eval-name">{m_name}: <span class="eval-score">{score:.0f}</span></div>
                        """, unsafe_allow_html=True)
                        
                        st.progress(score / 100)
                        
                        st.markdown(f"""
                            <p style="font-size:0.875rem; color:var(--text-secondary); margin-top:0.5rem;">{explanations.get(metric, '')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("---")
                    overall = metrics.overall_score
                    emoji = "🟢" if overall >= 80 else "🟡" if overall >= 60 else "🔴"
                    st.markdown(f"""
                    <div class="content-section">
                        <h2>{emoji} Overall Quality Score: {overall:.1f}/100</h2>
                        <p style='color:var(--text-secondary); margin-top:0.5rem;'>
                        Weighted average of all quality metrics - your total research score.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.warning(f"Evaluation unavailable: {str(e)}")

        except Exception as e:
            st.error(f"❌ Research failed: {str(e)}")
            with st.expander("Show error details"):
                st.exception(e)

# Tab 2 - Find Related
with tab2:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔍 Find Related Research</div>', unsafe_allow_html=True)
    
    related_query = st.text_input(
        "Search Query",
        placeholder="Enter keywords or topic to find related research",
        label_visibility="collapsed"
    )
    
    if st.button("🔎 Search Related", use_container_width=True):
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
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3 - Past Sessions
with tab3:
    st.markdown('<div class="section-title">📂 Past Research Sessions</div>', unsafe_allow_html=True)
    
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
                        
                        st.download_button(
                            "📥 Download",
                            json.dumps(data, indent=2),
                            json_file.name,
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Error loading {json_file.name}")
        else:
            st.info("📭 No past sessions found. Start your first research!")
    else:
        st.info("📭 No research history yet.")

# Footer
st.markdown("""
<div class="footer">
    <strong>AI Research Assistant v2.0</strong><br>
    Multi-Agent System • Powered by Claude & Tavily<br>
    Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
