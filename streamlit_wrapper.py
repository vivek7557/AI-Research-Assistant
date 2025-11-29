"""
Streamlit Web Interface for AI Research Assistant
Ultra-polished SaaS-style UI – 100 % logic-compatible
"""
import streamlit as st
import os, sys, json, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

# --------------  BUSINESS LOGIC IMPORTS (UNCHANGED) --------------
from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator
from memory.memory_bank import MemoryBank

# --------------  PAGE CONFIG  --------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------  GLOBAL CSS (SELF-CONTAINED) --------------
st.markdown(
    """
<style>
/* ---------- ROOT TOKENS ---------- */
:root{
    --bg0:#0e0e17;
    --bg1:#15151f;
    --bg2:#1c1c27;
    --bg3:#232330;
    --accent:#6366f1;
    --accent-dark:#4f46e5;
    --text1:#f2f2f7;
    --text2:#a0a0b4;
    --green:#10b981;
    --yellow:#f59e0b;
    --red:#ef4444;
    --border:#2a2a38;
    --radius:14px;
    --shadow:0 8px 32px rgba(0,0,0,.32);
    --font:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}

/* ---------- RESET ---------- */
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}
body{
    font-family:var(--font);
    background:var(--bg0);
    color:var(--text1);
}

/* ---------- MAIN LAYOUT ---------- */
.main .block-container{
    padding:2rem 3rem 4rem 3rem !important;
    max-width:1440px !important;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"]{
    background:var(--bg1);
    border-right:1px solid var(--border);
}
section[data-testid="stSidebar"] > div{
    padding:2rem 1.5rem;
}

/* ---------- CARDS ---------- */
.card{
    background:var(--bg2);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1.5rem;
    margin-bottom:1rem;
    transition:all .25s ease;
}
.card:hover{
    border-color:var(--accent);
    transform:translateY(-2px);
    box-shadow:var(--shadow);
}

/* ---------- HERO ---------- */
.hero{
    text-align:center;
    padding:4rem 0 3rem 0;
}
.hero h1{
    font-size:3rem;
    font-weight:800;
    background:linear-gradient(90deg,var(--accent) 0%,#8b5cf6 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:.25rem;
}
.hero p{
    font-size:1.1rem;
    color:var(--text2);
}

/* ---------- TABS ---------- */
.stTabs [data-baseweb="tab-list"]{
    gap:.75rem;
    background:transparent;
    border-bottom:1px solid var(--border);
    padding-bottom:.5rem;
}
.stTabs [data-baseweb="tab"]{
    background:var(--bg2);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:.5rem 1.25rem;
    font-weight:600;
    color:var(--text2);
    transition:all .2s ease;
}
.stTabs [data-baseweb="tab"]:hover{
    border-color:var(--accent);
}
.stTabs [aria-selected="true"]{
    background:var(--accent) !important;
    color:#fff !important;
    border-color:var(--accent) !important;
}

/* ---------- INPUTS ---------- */
.stTextInput input, .stSelectbox select{
    background:var(--bg0);
    border:1px solid var(--border);
    border-radius:var(--radius);
    color:var(--text1);
    padding:.75rem 1rem;
    font-size:1rem;
}
.stTextInput input:focus, .stSelectbox select:focus{
    border-color:var(--accent);
    box-shadow:0 0 0 2px rgba(99,102,241,.35);
}

/* ---------- BUTTONS ---------- */
.stButton > button{
    background:var(--accent);
    color:#fff;
    border:none;
    border-radius:var(--radius);
    padding:.75rem 1.5rem;
    font-weight:600;
    transition:all .2s ease;
}
.stButton > button:hover{
    background:var(--accent-dark);
    transform:translateY(-2px);
}

/* ---------- METRIC ---------- */
.metric{
    text-align:center;
}
.metric .label{
    font-size:.875rem;
    color:var(--text2);
    margin-bottom:.25rem;
}
.metric .value{
    font-size:2.25rem;
    font-weight:700;
    color:var(--text1);
}

/* ---------- FOOTER ---------- */
footer{
    text-align:center;
    padding:2.5rem 0 2rem 0;
    font-size:.875rem;
    color:var(--text2);
    border-top:1px solid var(--border);
    margin-top:4rem;
}
</style>""",
    unsafe_allow_html=True,
)

# --------------  SIDEBAR  --------------
with st.sidebar:
    st.markdown("### 📊 Research Analytics")
    try:
        stats = MemoryBank().get_statistics()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f'<div class="card metric"><div class="label">Total Research</div><div class="value">{stats.get("total_memories",0)}</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="card metric"><div class="label">Completed</div><div class="value">{stats.get("completed_sessions",0)}</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="card metric"><div class="label">Sources</div><div class="value">{stats.get("total_sources",0)}</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="card metric"><div class="label">Avg Quality</div><div class="value">{stats.get("avg_importance",0):.1f}/10</div></div>',
                unsafe_allow_html=True,
            )
    except Exception:
        st.info("Stats will appear after first research.")

    st.markdown("### 📈 Recent Activity")
    out_dir = Path("outputs")
    if out_dir.exists():
        files = sorted(out_dir.glob("*.json"), key=os.path.getmtime, reverse=True)[:6]
        for f in files:
            try:
                q = json.loads(f.read_text()).get("query", "Untitled")
                st.markdown(f"• {q[:32]}…")
            except Exception:
                pass
    else:
        st.markdown("No activity yet")

# --------------  API KEYS  --------------
anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "")
if anthropic_key:
    os.environ["ANTHROPIC_API_KEY"] = anthropic_key
if tavily_key:
    os.environ["TAVILY_API_KEY"] = tavily_key
keys_set = bool(anthropic_key and tavily_key)

# --------------  HERO  --------------
st.markdown(
    '<div class="hero"><h1>🔍 AI Research Assistant</h1><p>Deep, multi-agent research at your fingertips</p></div>',
    unsafe_allow_html=True,
)

# --------------  TABS  --------------
tab1, tab2, tab3 = st.tabs(["🔬 New Research", "🔍 Find Related", "📂 Past Sessions"])

# ---------- TAB 1 : NEW RESEARCH ----------
with tab1:
    if not keys_set:
        st.error("⚠️  Add ANTHROPIC_API_KEY and TAVILY_API_KEY to your `.env` file.")
        st.stop()

    with st.form("research_form"):
        query = st.text_input(
            "Research Query",
            placeholder="e.g., Impact of artificial intelligence on healthcare systems",
        )
        col_format, col_eval = st.columns([3, 2])
        with col_format:
            output_format = st.selectbox("Output Format", ["report", "article", "summary", "presentation"])
        with col_eval:
            run_evaluation = st.checkbox("Run Evaluation", value=True)
        with st.expander("Advanced Options"):
            session_id_input = st.text_input("Resume Session ID", placeholder="research_xxxxx")
            depth_level = st.slider("Research Depth", 1, 5, 3)
        submitted = st.form_submit_button("🚀 Start Research", use_container_width=True)

    if submitted and query:
        progress = st.progress(0)
        status = st.empty()
        try:
            status.info("🎯 Initializing agents…")
            progress.progress(20)
            orch = ResearchOrchestrator()

            status.info("📋 Planning strategy…")
            progress.progress(40)

            status.info("🔍 Conducting research…")
            progress.progress(60)
            results = orch.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id_input or None,
            )

            status.info("✅ Finalising report…")
            progress.progress(100)
            time.sleep(0.3)
            progress.empty()
            status.empty()
            st.success("✅ Research completed!")

            # metrics
            summary = results.get("research_summary", {})
            validation = results.get("validation", {})
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Sources", summary.get("total_sources", 0))
            c2.metric("Iterations", summary.get("iterations", 0))
            c3.metric("Confidence", f"{validation.get('confidence_score',0)}%")
            c4.metric("Format", output_format.title())

            # content
            content = results.get("final_content", {}).get("content", "")
            st.markdown(content)

            # downloads
            d1, d2, d3 = st.columns(3)
            d1.download_button("📥 Markdown", data=content, file_name="research.md", use_container_width=True)
            d2.download_button("📥 JSON", data=json.dumps(results, indent=2), file_name="research.json", use_container_width=True)
            d3.download_button("📥 TXT", data=content, file_name="research.txt", use_container_width=True)

            # evaluation
            if run_evaluation:
                evaluator = ResearchEvaluator()
                metrics = evaluator.evaluate_research(query, results)
                overall = metrics.overall_score
                st.markdown("---")
                st.subheader(f"📊 Quality Score – {overall:.1f}/100")
                for k, v in metrics.to_dict().items():
                    st.write(f"**{k.replace('_',' ').title()}** – {v:.0f}/100")
                    st.progress(v / 100)

        except Exception as e:
            st.error(f"❌ Research failed: {e}")
            with st.expander("Show traceback"):
                st.exception(e)

# ---------- TAB 2 : FIND RELATED ----------
with tab2:
    st.markdown("### 🔍 Find Related Research")
    related_query = st.text_input("Search Query", placeholder="Enter keywords…")
    if st.button("🔎 Search", use_container_width=True) and related_query:
        try:
            related = MemoryBank().get_related_research(related_query, limit=10)
            if related:
                st.success(f"Found {len(related)} related sessions")
                for r in related:
                    with st.expander(r.get("query", "Untitled")):
                        st.write("ID:", r.get("id", "N/A")[:12] + "…")
                        st.write("Sources:", r.get("sources_count", 0))
            else:
                st.info("No matches – try different keywords.")
        except Exception as e:
            st.error(f"Search failed: {e}")

# ---------- TAB 3 : PAST SESSIONS ----------
with tab3:
    st.markdown("### 📂 Past Research Sessions")
    if out_dir.exists():
        files = sorted(out_dir.glob("*.json"), key=os.path.getmtime, reverse=True)[:20]
        if files:
            for f in files:
                try:
                    data = json.loads(f.read_text())
                    with st.expander(data.get("query", "Untitled")):
                        c1, c2 = st.columns(2)
                        c1.write("**ID:** " + data.get("session_id", "N/A")[:12] + "…")
                        summary = data.get("research_summary", {})
                        c2.write("**Sources:** " + str(summary.get("total_sources", 0)))
                        st.download_button("📥 Download", json.dumps(data, indent=2), f.name, use_container_width=True)
                except Exception:
                    pass
        else:
            st.info("No past sessions – start your first research!")
    else:
        st.info("No history yet.")

# --------------  FOOTER  --------------
st.markdown(
    '<footer><strong>AI Research Assistant v2.0</strong><br>Multi-Agent System • Powered by Claude & Tavily</footer>',
    unsafe_allow_html=True,
)
