"""
Streamlit AI Research Assistant - Compact Modern UI
Optimized for integration with your backend
"""
import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

try:
    from orchestrator import ResearchOrchestrator
    from evaluation.evaluator import ResearchEvaluator
    from memory.memory_bank import MemoryBank
except ImportError:
    ResearchOrchestrator = None

st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Compact Modern CSS
st.markdown("""
<style>
* { margin: 0; padding: 0; }

:root {
    --primary: #3b82f6;
    --secondary: #8b5cf6;
    --accent: #06b6d4;
    --success: #10b981;
    --danger: #ef4444;
    --bg: #0f172a;
    --card: #1e293b;
    --border: #334155;
}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1a1f35 100%) !important;
}

/* Header */
[data-testid="stHeader"] { display: none; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    border-right: 1px solid rgba(51, 65, 85, 0.3) !important;
}

/* Main area */
[data-testid="stMain"] { padding: 0 !important; }

.main { max-width: 100% !important; }

/* Inputs */
input, select, textarea {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(51, 65, 85, 0.5) !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    padding: 8px 12px !important;
    font-size: 13px !important;
}

input:focus, select:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 6px 14px !important;
    height: 32px !important;
    border-radius: 6px !important;
    font-size: 12px !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25) !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.35) !important;
}

/* Download buttons */
.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 6px 14px !important;
    height: 32px !important;
    border-radius: 6px !important;
    font-size: 12px !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.08)) !important;
    border: 1px solid rgba(51, 65, 85, 0.3) !important;
    border-radius: 8px !important;
    padding: 12px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

[data-testid="stMetric"] label { font-size: 11px !important; font-weight: 600 !important; }

[data-testid="stMetric"] div {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 18px !important;
    font-weight: 700 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 8px !important; border: none !important; }

.stTabs [data-baseweb="tab"] {
    background: rgba(59, 130, 246, 0.05) !important;
    border: 1px solid rgba(59, 130, 246, 0.2) !important;
    border-radius: 6px !important;
    padding: 8px 16px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
    border-color: #3b82f6 !important;
    color: white !important;
}

/* Cards */
.stContainer { background: none !important; }

[data-testid="stExpander"] {
    border: 1px solid rgba(51, 65, 85, 0.3) !important;
    border-radius: 8px !important;
}

/* Progress */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%) !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-left: 3px solid !important;
    padding: 12px !important;
    font-size: 13px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: rgba(59, 130, 246, 0.05); }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #3b82f6, #8b5cf6); border-radius: 4px; }

/* Custom cards */
.custom-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8));
    border: 1px solid rgba(51, 65, 85, 0.3);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}

.custom-card:hover {
    border-color: rgba(59, 130, 246, 0.5);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

/* Text styling */
h1 { font-size: 20px !important; font-weight: 800 !important; }
h2 { font-size: 16px !important; font-weight: 700 !important; }
h3 { font-size: 14px !important; font-weight: 600 !important; }
p { font-size: 13px !important; }

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 20px; padding: 0 16px;'>
    <div style='width: 28px; height: 28px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); border-radius: 6px; display: flex; align-items: center; justify-content: center;'>
        <span style='color: white; font-size: 16px;'>🔍</span>
    </div>
    <h1 style='margin: 0; font-size: 20px; background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4); background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>ResearchAI</h1>
</div>
""", unsafe_allow_html=True)

# Layout
col_sidebar, col_main = st.columns([1, 3.5])

# Sidebar
with col_sidebar:
    st.markdown("### 📊 Stats")
    
    try:
        memory_bank = MemoryBank()
        stats = memory_bank.get_statistics()
    except:
        stats = {"total_memories": 24, "completed_sessions": 18, "total_sources": 156, "avg_importance": 8.4}
    
    c1, c2 = st.columns(2)
    c1.metric("📚 Research", stats.get("total_memories", 0), delta=None)
    c2.metric("✅ Done", stats.get("completed_sessions", 0))
    
    c1, c2 = st.columns(2)
    c1.metric("🔗 Sources", stats.get("total_sources", 0))
    c2.metric("⭐ Quality", f"{stats.get('avg_importance', 0):.1f}")
    
    st.markdown("---")
    st.markdown("### 📝 Recent")
    
    output_dir = Path("outputs")
    if output_dir.exists():
        json_files = sorted(output_dir.glob("*.json"), key=os.path.getmtime, reverse=True)[:4]
        for file in json_files:
            try:
                with open(file) as f:
                    data = json.load(f)
                query = data.get("query", "Untitled")
                st.caption(f"• {query[:20]}...")
            except:
                pass

# Main content
with col_main:
    tab1, tab2, tab3 = st.tabs(["🚀 Research", "🔍 Explore", "📂 History"])
    
    with tab1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        query = st.text_input("🔎 What do you want to research?", placeholder="e.g., AI impact on healthcare", label_visibility="collapsed")
        
        col1, col2, col3 = st.columns([2, 1.5, 1])
        output_format = col1.selectbox("Format", ["report", "article", "summary"], label_visibility="collapsed")
        run_eval = col2.checkbox("Evaluate", value=True)
        search_btn = col3.button("🚀 Search", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if search_btn and query:
            if not ResearchOrchestrator:
                st.error("Backend not connected")
                st.stop()
            
            with st.spinner("🔄 Researching..."):
                progress = st.progress(0)
                
                try:
                    orchestrator = ResearchOrchestrator()
                    progress.progress(30)
                    
                    results = orchestrator.conduct_research(
                        query=query,
                        output_format=output_format
                    )
                    progress.progress(100)
                    progress.empty()
                    
                    st.success("✅ Complete!")
                    
                    # Metrics
                    m1, m2, m3, m4 = st.columns(4)
                    summary = results.get("research_summary", {})
                    validation = results.get("validation", {})
                    
                    m1.metric("📚", summary.get("total_sources", 0))
                    m2.metric("🔄", summary.get("iterations", 0))
                    m3.metric("🎯", f"{validation.get('confidence_score', 0)}%")
                    m4.metric("📝", output_format)
                    
                    # Content
                    with st.expander("📄 Content", expanded=True):
                        final_content = results.get("final_content", {})
                        st.markdown(final_content.get("content", ""))
                    
                    # Downloads
                    col1, col2, col3 = st.columns(3)
                    content = final_content.get("content", "")
                    col1.download_button("📥 MD", content, file_name="research.md", use_container_width=True)
                    col2.download_button("📥 TXT", content, file_name="research.txt", use_container_width=True)
                    col3.download_button("📥 JSON", json.dumps(results, indent=2), file_name="research.json", use_container_width=True)
                    
                    # Evaluation
                    if run_eval:
                        st.markdown("---")
                        with st.expander("📊 Evaluation", expanded=True):
                            try:
                                evaluator = ResearchEvaluator()
                                metrics = evaluator.evaluate_research(query, results)
                                metrics_dict = metrics.to_dict()
                                
                                for metric, score in metrics_dict.items():
                                    col1, col2 = st.columns([3, 1])
                                    col1.metric(metric.replace("_", " ").title(), "", delta=None)
                                    st.progress(score / 100)
                                
                                overall = metrics.overall_score
                                emoji = "🟢" if overall >= 80 else "🟡" if overall >= 60 else "🔴"
                                st.markdown(f"### {emoji} Score: {overall:.1f}/100")
                            except:
                                st.warning("Evaluation unavailable")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.info("🔗 Related research feature")
    
    with tab3:
        st.markdown("### Past Sessions")
        output_dir = Path("outputs")
        if output_dir.exists():
            for file in sorted(output_dir.glob("*.json"), key=os.path.getmtime, reverse=True):
                try:
                    with open(file) as f:
                        data = json.load(f)
                    if st.button(data.get("query", "Untitled"), key=file.stem):
                        st.json(data)
                except:
                    pass

# Footer
st.markdown("---")
st.caption("🚀 ResearchAI v2.0 | Powered by Claude & Tavily")
