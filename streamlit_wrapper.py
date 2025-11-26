"""
Streamlit Web Interface for AI Research Assistant
Modern UI with centered layout and comprehensive analysis
FIXED: Depth parameter fully integrated
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

# === PAGE CONFIG WITH MODERN THEME ===
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# === MINIMAL, HIGH-IMPACT CSS ===
st.markdown("""
<style>
/* Reduce Streamlit's default padding */
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 1100px !important;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border-radius: 16px;
    padding: 1.4rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
}

.main-header h1 {
    font-size: 1.9rem;
    font-weight: 700;
    background: linear-gradient(90deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}

.main-header p {
    color: #94a3b8;
    font-size: 0.98rem;
    margin-top: 0.3rem;
}

/* Input container */
.input-container {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.3rem;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);
}

/* Buttons - clean and light */
.stButton > button {
    height: 2.3rem;
    padding: 0 1.3rem;
    font-size: 0.92rem;
    font-weight: 600;
    border-radius: 8px;
    background: linear-gradient(to right, #6366f1, #8b5cf6);
    color: white;
    border: none;
    box-shadow: 0 2px 6px rgba(99, 102, 241, 0.25);
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(99, 102, 241, 0.35);
}

/* Download buttons */
.stDownloadButton > button {
    height: 2.2rem;
    font-size: 0.86rem;
    padding: 0 1.1rem;
    border-radius: 7px;
    background: #1e293b;
    color: #cbd5e1;
    border: 1px solid #334155;
}
.stDownloadButton > button:hover {
    background: #334155;
    color: white;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.8rem;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    background: #1e293b;
    padding: 0.6rem 1.3rem;
    border-radius: 10px;
    border: 1px solid #334155;
    font-weight: 600;
    font-size: 0.93rem;
    color: #cbd5e1;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #334155;
    border-color: #818cf8;
    color: white;
    box-shadow: 0 2px 6px rgba(129, 140, 248, 0.2);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0b111f;
}
.sidebar-card {
    background: #121d2f;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.9rem;
}
.sidebar-title { font-size: 0.82rem; color: #94a3b8; margin-bottom: 3px; }
.sidebar-value { font-size: 1.3rem; font-weight: 700; color: #e2e8f0; }
.sidebar-activity-title { margin-top: 1.2rem; font-size: 0.92rem; font-weight: 700; color: #cbd5e1; }
.sidebar-activity-item { font-size: 0.82rem; color: #94a3b8; margin-bottom: 5px; }

/* Metrics */
[data-testid="stMetric"] {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 0.85rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

/* Progress bar */
.stProgress > div > div {
    height: 5px !important;
    background-color: #818cf8 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.9rem;
    padding-top: 1.2rem;
    margin-top: 1rem;
    border-top: 1px solid #1e293b;
}
</style>
""", unsafe_allow_html=True)

# =============== SIDEBAR ===============
with st.sidebar:
    st.markdown("### 📊 Research Analytics")
    try:
        memory_bank = MemoryBank()
        stats = memory_bank.get_statistics()
        for title, key, fmt in [
            ("📚 Total Research", "total_memories", "d"),
            ("✅ Completed", "completed_sessions", "d"),
            ("🔗 Total Sources", "total_sources", "d"),
            ("⭐ Avg Quality", "avg_importance", ".1f")
        ]:
            val = stats.get(key, 0)
            if "Avg" in title:
                val = f"{val:.1f}/10"
            st.markdown(f"""
            <div class="sidebar-card">
                <div class="sidebar-title">{title}</div>
                <div class="sidebar-value">{val}</div>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.info("Stats appear after first run")

    st.markdown("<div class='sidebar-activity-title'>📝 Recent Activity</div>", unsafe_allow_html=True)
    output_dir = Path("outputs")
    if output_dir.exists():
        files = sorted(output_dir.glob("*.json"), key=os.path.getmtime, reverse=True)[:6]
        for f in files:
            try:
                with open(f) as fd:
                    q = json.load(fd).get("query", "")[:32] + "..."
                st.markdown(f"<div class='sidebar-activity-item'>• {q}</div>", unsafe_allow_html=True)
            except:
                pass
    else:
        st.markdown("<div class='sidebar-activity-item'>No activity yet</div>", unsafe_allow_html=True)

# =============== API KEYS ===============
try:
    anthropic_key = st.secrets["ANTHROPIC_API_KEY"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    tavily_key = st.secrets["TAVILY_API_KEY"]
    keys_set = True
except KeyError:
    keys_set = False

# =============== MAIN HEADER ===============
st.markdown("""
<div class="main-header">
    <h1>🔍 AI Research Assistant</h1>
    <p>Deep research powered by multi-agent AI system</p>
</div>
""", unsafe_allow_html=True)

# =============== TABS ===============
tab1, tab2, tab3 = st.tabs(["🔬 New Research", "🔍 Find Related", "📂 Past Sessions"])

# =============== TAB 1: NEW RESEARCH ===============
with tab1:
    if not keys_set:
        st.error("⚠️ API Keys missing in .env")
        st.stop()

    _, center, _ = st.columns([1, 8, 1])
    with center:
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        
        # Search Query
        query = st.text_input(
            "🔎 Research Query",
            placeholder="e.g., Impact of AI on healthcare",
            label_visibility="collapsed"
        )
        
        # Output Format & Evaluation
        col1, col2 = st.columns([3, 2])
        output_format = col1.selectbox(
            "📄 Output Format",
            ["report", "article", "summary", "presentation"],
            label_visibility="collapsed"
        )
        run_evaluation = col2.checkbox("🎯 Run Evaluation", value=True)
        
        # Advanced Options
        with st.expander("⚙️ Advanced Options"):
            c1, c2 = st.columns(2)
            session_id = c1.text_input("Resume Session ID", placeholder="research_xxxx")
            depth = c2.slider("Research Depth", 1, 5, 3)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # =============== START RESEARCH BUTTON ===============
        if st.button("🚀 Start Research", use_container_width=True):
            if not query.strip():
                st.warning("Please enter a research query.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.info("Initializing...")
                    progress_bar.progress(20)
                    orchestrator = ResearchOrchestrator()
                    
                    status_text.info("Planning research...")
                    progress_bar.progress(40)
                    
                    status_text.info("Running agents with depth level " + str(depth) + "...")
                    progress_bar.progress(60)
                    
                    # ✅ DEPTH PARAMETER ADDED HERE
                    results = orchestrator.conduct_research(
                        query=query,
                        output_format=output_format,
                        session_id=session_id or None,
                        depth=depth
                    )
                    
                    status_text.info("Finalizing...")
                    progress_bar.progress(100)
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.success("✅ Research completed successfully!")

                    # =============== METRICS ===============
                    st.markdown("---")
                    st.markdown("### 📊 Research Metrics")
                    final_content = results.get("final_content", {})
                    summary = results.get("research_summary", {})
                    validation = results.get("validation", {})
                    
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("📚 Sources", summary.get("total_sources", 0))
                    c2.metric("🔄 Iterations", summary.get("iterations", 0))
                    c3.metric("🎯 Confidence", f"{validation.get('confidence_score', 0)}%")
                    c4.metric("📝 Format", output_format.title())

                    # =============== RESEARCH CONTENT ===============
                    st.markdown("---")
                    st.markdown("### 📄 Generated Research")
                    content = final_content.get("content", "")
                    st.markdown(content)

                    # =============== DOWNLOAD OPTIONS ===============
                    st.markdown("---")
                    d1, d2, d3 = st.columns(3)
                    d1.download_button(
                        "📥 Markdown",
                        data=content,
                        file_name="research.md"
                    )
                    d2.download_button(
                        "📥 JSON",
                        data=json.dumps(results, indent=2),
                        file_name="research.json"
                    )
                    d3.download_button(
                        "📥 TXT",
                        data=content,
                        file_name="research.txt"
                    )

                    # =============== EVALUATION ===============
                    if run_evaluation:
                        st.markdown("---")
                        st.markdown("### 📊 Quality Evaluation")
                        try:
                            evaluator = ResearchEvaluator()
                            metrics = evaluator.evaluate_research(query, results)
                            
                            explanations = {
                                "completeness": "Measures how fully the research covers all important aspects...",
                                "accuracy": "Checks how factually correct the statements are...",
                                "relevance": "Evaluates how closely the content matches the query...",
                                "quality": "Judges structure, clarity, and flow of writing...",
                                "efficiency": "Measures how well the system used sources...",
                                "citations": "Evaluates whether sources are properly referenced...",
                                "overall": "Weighted average of all metrics — your total quality score.",
                            }
                            
                            for metric, score in metrics.to_dict().items():
                                m_name = metric.replace("_", " ").title()
                                left, right = st.columns([4, 1])
                                
                                with left:
                                    st.markdown(f"**{m_name}**")
                                    st.progress(score / 100)
                                    st.markdown(
                                        f"<p style='font-size:0.85rem; color:#94a3b8;'>{explanations.get(metric, '')}</p>",
                                        unsafe_allow_html=True
                                    )
                                
                                with right:
                                    st.markdown(
                                        f"<div style='text-align:center; padding:0.5rem;'><div style='font-size:0.8rem; color:#94a3b8;'>{m_name}</div><div style='font-size:1.3rem; font-weight:700; color:#e2e8f0;'>{score}</div></div>",
                                        unsafe_allow_html=True
                                    )
                            
                            st.markdown("---")
                            overall = metrics.overall_score
                            emoji = "🟢" if overall >= 80 else "🟡" if overall >= 60 else "🔴"
                            st.markdown(
                                f"<h3>{emoji} Overall Quality Score: {overall:.1f}/100</h3><p style='color:#94a3b8; font-size:0.9rem;'>{explanations['overall']}</p>",
                                unsafe_allow_html=True
                            )
                        
                        except Exception as e:
                            st.warning(f"Evaluation unavailable: {str(e)}")
                
                except Exception as e:
                    st.error(f"❌ Error during research: {str(e)}")

# =============== TAB 2: FIND RELATED ===============
with tab2:
    st.markdown("### 🔗 Find Related Research")
    search_query = st.text_input("Search related topics", placeholder="Enter a topic...")
    if search_query:
        st.info("Related research feature coming soon...")

# =============== TAB 3: PAST SESSIONS ===============
with tab3:
    st.markdown("### 📂 Past Research Sessions")
    output_dir = Path("outputs")
    
    if output_dir.exists():
        files = sorted(output_dir.glob("*.json"), key=os.path.getmtime, reverse=True)
        if files:
            for f in files:
                try:
                    with open(f) as fd:
                        data = json.load(fd)
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{data.get('query', 'Untitled')}**")
                    with col2:
                        if st.button("View", key=f"view_{f.stem}"):
                            st.json(data)
                except:
                    pass
        else:
            st.info("No past sessions found")
    else:
        st.info("No sessions directory yet")

# =============== FOOTER ===============
st.markdown(
    '<div class="footer">AI Research Assistant v2.0 • Multi-Agent System<br>Powered by Claude & Tavily</div>',
    unsafe_allow_html=True
)
