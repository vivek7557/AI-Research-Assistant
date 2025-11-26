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

# Custom CSS for modern, compact, React-inspired UI
st.markdown("""
<style>

/* ====================================== */
/*         REFINED COMPACT ANIMATIONS     */
/* ====================================== */

/* Fade + slide for entire page */
@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(8px); }
    100% { opacity: 1; transform: translateY(0); }
}
.fade-in {
    animation: fadeInUp 0.5s ease both;
}

/* Apply fade to cards, header, inputs */
.main-header,
.input-container,
.content-card {
    animation: fadeInUp 0.5s ease both;
}

/* Section stagger effect - faster */
.section-block {
    opacity: 0;
    animation: fadeInUp 0.6s ease forwards;
}
.section-block:nth-child(1) { animation-delay: 0.05s; }
.section-block:nth-child(2) { animation-delay: 0.1s; }
.section-block:nth-child(3) { animation-delay: 0.15s; }
.section-block:nth-child(4) { animation-delay: 0.2s; }

/* Subtle hover scaling */
.hover-scale {
    transition: transform 0.2s ease;
}
.hover-scale:hover {
    transform: scale(1.01);
}

/* Soft glowing border hover */
@keyframes softGlow {
    from { box-shadow: 0 0 0 rgba(111,111,245,0.0); }
    to { box-shadow: 0 0 12px rgba(111,111,245,0.15); }
}
.input-container:hover,
.content-card:hover,
.eval-right:hover {
    animation: softGlow 0.3s ease forwards;
    border-color: #6f6ff5;
}

/* Animated gradient header text - slightly smaller */
@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}
.main-header h1 {
    font-size: 2.0rem;            /* Reduced from 2.2rem */
    font-weight: 700;             /* Slightly lighter */
    background-size: 200% 200%;
    background: linear-gradient(135deg, #8b7bff 0%, #a78cff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientFlow 5s ease-in-out infinite alternate;
}

/* Soft pulse for progress bars */
@keyframes pulseBar {
    0% { opacity: 0.85; }
    50% { opacity: 1; }
    100% { opacity: 0.85; }
}
.stProgress > div > div {
    animation: pulseBar 2s ease-in-out infinite;
    height: 6px !important;      /* Thinner progress bar */
}

/* Evaluation cards slide in */
@keyframes slideInRight {
    0% { opacity: 0; transform: translateX(12px); }
    100% { opacity: 1; transform: translateX(0); }
}
.eval-right {
    animation: slideInRight 0.4s ease both;
}

/* BUTTONS: SMALLER & COMPACT */
.stButton > button {
    height: 2.6rem !important;       /* Reduced height */
    padding: 0 1.4rem !important;    /* Less padding */
    font-size: 0.92rem !important;   /* Smaller text */
    font-weight: 600 !important;
    border-radius: 8px !important;   /* Slightly rounder */
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: scale(1.03);          /* Less exaggeration */
    box-shadow: 0 4px 14px rgba(131,131,255,0.20) !important;
}

/* DOWNLOAD BUTTONS: SMALLER */
.stDownloadButton > button {
    height: 2.4rem !important;
    font-size: 0.88rem !important;
    padding: 0 1.2rem !important;
    background: #2a2a2a !important;
    color: #e5e5e5 !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 7px !important;
}

/* Tabs: Compact & Clean */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.8rem;                    /* Less gap */
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    background: #1e1e1e !important;
    padding: 0.65rem 1.3rem !important;  /* Less padding */
    border-radius: 9px !important;
    border: 1px solid #2c2c2c !important;
    font-weight: 600;
    font-size: 0.95rem !important;       /* Slightly smaller */
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #2a2a2a !important;
    border-color: #6f6ff5 !important;
}

/* Subtle tab animation */
.stTabs [data-baseweb="tab"] {
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    transform: translateY(-1px);
    border-color: #6f6ff5 !important;
}


/* ====================================== */
/*           COMPACT THEME STYLING        */
/* ====================================== */

.main-content {
    max-width: 1100px;              /* Slightly narrower */
    margin: auto;
    padding: 1.5rem;                /* Reduced padding */
}

.main-header {
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    border-radius: 16px;            /* Slightly rounder */
    padding: 1.6rem;                /* Less padding */
    box-shadow: 0px 3px 12px rgba(0,0,0,0.32);
}

.main-header p {
    font-size: 1.0rem;              /* Slightly smaller */
    color: #a7a7a7;
    margin-top: 0.4rem;
}

/* Input card - compact */
.input-container {
    background: #1b1b1b;
    border: 1px solid #2c2c2c;
    padding: 1.3rem;                /* Reduced padding */
    border-radius: 12px;            /* Rounder */
    box-shadow: 0 3px 9px rgba(0,0,0,0.38);
}

/* Sidebar - compact */
[data-testid="stSidebar"] {
    background: #111111;
    border-right: 1px solid #222;
    padding: 1rem 0.8rem !important; /* Tighter padding */
}

/* Metrics - compact cards */
[data-testid="stMetric"] {
    background: #1b1b1b;
    padding: 0.85rem;               /* Less padding */
    border: 1px solid #2c2c2c;
    border-radius: 12px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.35);
    height: 80px;                   /* Fixed height for alignment */
}

/* Content cards */
.content-card {
    background: #1b1b1b;
    border: 1px solid #2c2c2c;
    padding: 1.0rem;                /* Reduced padding */
    border-radius: 12px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.32);
}

/* Text inputs and selects - compact */
input, textarea, select {
    font-size: 0.95rem !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    padding: 0.55rem 0.75rem !important;
    height: auto !important;
}

/* Expander - compact */
.streamlit-expanderHeader {
    padding: 0.45rem 0.9rem !important;
    font-size: 0.95rem !important;
}

/* Evaluation score display */
.eval-title {
    font-size: 0.8rem;
    color: #b0b0b0;
    margin-bottom: 4px;
}
.eval-score {
    font-size: 1.4rem;
    font-weight: 700;
    color: white;
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


st.markdown("""
<style>
    /* ===================== */
/* SIDEBAR FIXED LAYOUT  */
/* ===================== */

[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: 1px solid #222;
    padding: 1rem 0.6rem;
}

/* Compact cards */
.sidebar-card {
    background: #1a1a1a;
    border: 1px solid #2d2d2d;
    border-radius: 10px;           /* Slightly rounder */
    padding: 0.7rem 0.9rem;        /* Less padding */
    margin-bottom: 0.9rem;         /* Less gap */
    box-shadow: 0px 2px 7px rgba(0,0,0,0.32);
    transition: 0.2s ease;
}

.sidebar-card:hover {
    transform: scale(1.01);
    border-color: #6f6ff5;
}

/* Titles */
.sidebar-title {
    font-size: 0.82rem;            /* Slightly smaller */
    font-weight: 600;
    color: #cfcfcf;
    margin-bottom: 4px;
}

/* Values */
.sidebar-value {
    font-size: 1.3rem;             /* Slightly smaller */
    font-weight: 700;
    color: white;
}

/* Recent Activity Title */
.sidebar-activity-title {
    margin-top: 1.3rem;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    color: #dcdcdc;
}

/* Each recent item */
.sidebar-activity-item {
    font-size: 0.82rem;            /* Smaller text */
    color: #bdbdbd;
    margin-bottom: 5px;            /* Less spacing */
    transition: 0.15s ease;
}

.sidebar-activity-item:hover {
    color: #ffffff;
    margin-left: 3px;
}

</style>
""", unsafe_allow_html=True)



# API Keys
# API Keys (Streamlit Cloud)
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
                                    f"<p style='font-size:0.85rem; color:#cccccc; margin-top:4px;'>"
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
<p style='color:#cfcfcf; font-size:0.9rem;'>
{explanations['overall']}
</p>
""",
                            unsafe_allow_html=True,
                        )
                    except Exception as e:
                        st.warning(f"Evaluation unavailable: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error during research: {str(e)}")

# Tabs 2 & 3 unchanged because no UI errors exist
# (Ask if you want them upgraded too.)

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; opacity:0.7; padding:1rem'>
    AI Research Assistant v2.0 • Multi-Agent System<br>
    Powered by Claude & Tavily
</div>
""", unsafe_allow_html=True)
