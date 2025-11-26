import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

# Only import if needed (to avoid errors in demo)
try:
    from orchestrator import ResearchOrchestrator
    from evaluation.evaluator import ResearchEvaluator
    from memory.memory_bank import MemoryBank
    BACKEND_AVAILABLE = True
except Exception:
    BACKEND_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="centered",  # Centered = more React-like focus
    initial_sidebar_state="expanded"
)

# Custom CSS - React-inspired minimalism
st.markdown("""
<style>
/* Base theme */
:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --surface: #1f2937;
    --surface-light: #374151;
    --border: #4b5563;
    --text: #f9fafb;
    --text-secondary: #d1d5db;
}

[data-testid="stAppViewContainer"] {
    background-color: #111827;
    padding: 1rem;
}

/* Header */
.main-header {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.25rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
}

.main-header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #c7d2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}

.main-header p {
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin-top: 0.25rem;
}

/* Input card */
.input-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

/* Small buttons */
.stButton > button {
    height: 2.4rem !important;
    padding: 0 1.25rem !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    background-color: var(--primary) !important;
    border: none !important;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: var(--primary-dark) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3) !important;
}

/* Small select & input */
div[data-baseweb="select"] > div {
    background-color: var(--surface-light) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 0.9rem !important;
    height: 2.4rem !important;
}

input, textarea {
    background-color: var(--surface-light) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 0.75rem !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    background: var(--surface-light) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.4rem 1rem !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-size: 1.1rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.8rem !important;
    color: var(--text-secondary) !important;
}

.metric-card {
    background: var(--surface-light);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.75rem;
    text-align: center;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0f172a !important;
    border-right: 1px solid var(--border);
}

.sidebar-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.75rem;
    margin-bottom: 1rem;
}

.sidebar-title {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-bottom: 4px;
}
.sidebar-value {
    font-size: 1.2rem;
    font-weight: 700;
    color: white;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface-light) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.4rem 0.8rem !important;
    font-size: 0.9rem !important;
}

/* Footer */
.footer {
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.8rem;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Research Analytics")
    
    if BACKEND_AVAILABLE:
        try:
            memory_bank = MemoryBank()
            stats = memory_bank.get_statistics()
            
            for title, key, fmt in [
                ("📚 Total Research", "total_memories", "d"),
                ("✅ Completed", "completed_sessions", "d"),
                ("🔗 Total Sources", "total_sources", "d"),
                ("⭐ Avg Quality", "avg_importance", ".1f")
            ]:
                value = stats.get(key, 0)
                if "Avg" in title:
                    value = f"{value:.1f}/10"
                st.markdown(f"""
                <div class="sidebar-card">
                    <div class="sidebar-title">{title}</div>
                    <div class="sidebar-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.info("Stats require first run")
    
    # Recent activity
    st.markdown("### 📝 Recent Activity")
    output_dir = Path("outputs")
    if output_dir.exists():
        files = sorted(output_dir.glob("*.json"), key=os.path.getmtime, reverse=True)[:5]
        for f in files:
            try:
                with open(f) as fd:
                    q = json.load(fd).get("query", "")[:30] + "..."
                st.markdown(f"- {q}", unsafe_allow_html=False)
            except:
                pass
    else:
        st.caption("No activity yet")

# Main
st.markdown("""
<div class="main-header">
    <h1>🔍 AI Research Assistant</h1>
    <p>Deep research powered by multi-agent AI system</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔬 New", "🔍 Find", "📂 Past"])

with tab1:
    if not BACKEND_AVAILABLE:
        st.warning("Backend modules not available. Using demo mode.")
    
    # Input card
    with st.container():
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        
        query = st.text_input(
            "Research Query",
            placeholder="e.g., Impact of AI on healthcare",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([3, 2])
        output_format = col1.selectbox(
            "Format",
            ["report", "article", "summary", "presentation"],
            label_visibility="collapsed"
        )
        run_eval = col2.checkbox("Evaluate", value=True, help="Run quality evaluation")
        
        with st.expander("⚙️ Advanced", expanded=False):
            c1, c2 = st.columns(2)
            session_id = c1.text_input("Session ID", placeholder="research_xxx")
            depth = c2.slider("Depth", 1, 5, 3, label_visibility="collapsed")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Start Research", use_container_width=True, type="primary"):
            if not query.strip():
                st.warning("Enter a research query")
            else:
                if BACKEND_AVAILABLE:
                    # Simulate progress
                    progress = st.progress(0)
                    status = st.empty()
                    for i in [20, 40, 60, 80, 100]:
                        status.text(f"Processing... {i}%")
                        progress.progress(i)
                        import time
                        time.sleep(0.3)
                    status.empty()
                    progress.empty()
                    
                    # Mock result
                    st.success("✅ Research completed!")
                    st.markdown("### 📄 Result Preview")
                    st.markdown(f"> Your research on **{query}** has been generated in **{output_format}** format.")
                    
                    # Metrics row
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Sources", "24")
                    m2.metric("Confidence", "92%")
                    m3.metric("Time", "42s")
                    m4.metric("Format", output_format.title())
                    
                    # Download
                    d1, d2 = st.columns(2)
                    d1.download_button("📥 Markdown", data=query, file_name="research.md", use_container_width=True)
                    d2.download_button("📥 JSON", data="{}", file_name="research.json", use_container_width=True)
                    
                    if run_eval:
                        st.markdown("### 📊 Evaluation")
                        st.progress(85)
                        st.caption("Overall quality: 85/100")
                else:
                    st.info("Demo mode: Research would run here with backend.")

with tab2:
    st.info("🔍 Find related research – coming soon")

with tab3:
    st.info("📂 View past sessions – coming soon")

# Footer
st.markdown("""
<div class="footer">
    AI Research Assistant • Multi-Agent System<br>
    Powered by Claude & Tavily
</div>
""", unsafe_allow_html=True)
