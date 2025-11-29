"""
AI Research Assistant – Creative Edition
Ultra-modern glass-morphism UI (logic untouched)
"""
import streamlit as st
import os, sys, json, time, datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

# --------------  ORIGINAL IMPORTS  --------------
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

# --------------  GLOBAL GLASS-MORPHISM CSS  --------------
st.markdown(
    """
<style>
/* ---------- ROOT TOKENS ---------- */
:root{
    --bg0:#0c0c0f;
    --bg1:#111115;
    --bg2:#1a1a20;
    --bg3:#22222b;
    --glass:rgba(26,26,32,0.55);
    --accent:#00f5ff;
    --accent2:#ff00c1;
    --text1:#f0f0f5;
    --text2:#a0a0b3;
    --green:#00ff9d;
    --yellow:#ffd60a;
    --red:#ff3d3d;
    --radius:18px;
    --blur:16px;
    --glow:0 0 12px var(--accent);
    --font:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}

/* ---------- BACKDROP (AURORA) ---------- */
body{
    font-family:var(--font);
    background:var(--bg0);
    color:var(--text1);
    overflow-x:hidden;
}
body::before{
    content:"";
    position:fixed;
    top:0;left:0;width:100%;height:100%;
    background:
        radial-gradient(circle at 15% 30%, var(--accent) 0%, transparent 30%),
        radial-gradient(circle at 85% 70%, var(--accent2) 0%, transparent 30%);
    opacity:.13;
    animation:aurora 20s infinite alternate;
    z-index:-1;
}
@keyframes aurora{
    0%{transform:rotate(0deg) scale(1.2);}
    100%{transform:rotate(360deg) scale(1.4);}
}

/* ---------- GLASS CARD ---------- */
.glass{
    background:var(--glass);
    backdrop-filter:blur(var(--blur));
    -webkit-backdrop-filter:blur(var(--blur));
    border:1px solid rgba(255,255,255,.08);
    border-radius:var(--radius);
    padding:2rem;
    box-shadow:0 12px 40px rgba(0,0,0,.35);
    transition:all .3s ease;
}
.glass:hover{
    border-color:var(--accent);
    box-shadow:var(--glow),0 12px 40px rgba(0,0,0,.45);
    transform:translateY(-4px);
}

/* ---------- FLOATING HERO ---------- */
.hero{
    position:relative;
    text-align:center;
    padding:5rem 0 4rem 0;
}
.hero h1{
    font-size:3.5rem;
    font-weight:900;
    letter-spacing:-1px;
    background:linear-gradient(90deg,var(--accent),var(--accent2));
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation:float 4s ease-in-out infinite;
}
@keyframes float{
    0%,100%{transform:translateY(0);}
    50%{transform:translateY(-8px);}
}
.hero p{
    font-size:1.2rem;
    color:var(--text2);
    margin-top:.5rem;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"]{
    background:var(--bg1);
    border-right:1px solid rgba(255,255,255,.06);
}
section[data-testid="stSidebar"] > div{
    padding:2.5rem 1.75rem;
}

/* ---------- TABS ---------- */
.stTabs [data-baseweb="tab-list"]{
    gap:1rem;
    background:transparent;
    border-bottom:1px solid rgba(255,255,255,.06);
}
.stTabs [data-baseweb="tab"]{
    background:var(--glass);
    border:1px solid rgba(255,255,255,.06);
    border-radius:var(--radius);
    padding:.6rem 1.4rem;
    font-weight:600;
    color:var(--text2);
    transition:all .2s ease;
}
.stTabs [data-baseweb="tab"]:hover{
    border-color:var(--accent);
}
.stTabs [aria-selected="true"]{
    background:linear-gradient(90deg,var(--accent),var(--accent2));
    color:#fff;
    border-color:transparent;
    box-shadow:var(--glow);
}

/* ---------- INPUT ---------- */
.stTextInput input, .stSelectbox select{
    background:var(--bg1);
    border:1px solid rgba(255,255,255,.08);
    border-radius:var(--radius);
    color:var(--text1);
    padding:.75rem 1rem;
    font-size:1rem;
    transition:all .2s ease;
}
.stTextInput input:focus, .stSelectbox select:focus{
    border-color:var(--accent);
    box-shadow:var(--glow);
}

/* ---------- BUTTON ---------- */
.stButton > button{
    background:linear-gradient(90deg,var(--accent),var(--accent2));
    color:#fff;
    border:none;
    border-radius:var(--radius);
    padding:.8rem 2rem;
    font-weight:700;
    font-size:1rem;
    box-shadow:var(--glow);
    transition:all .25s ease;
}
.stButton > button:hover{
    transform:scale(1.05);
    box-shadow:0 0 20px var(--accent);
}

/* ---------- METRIC ---------- */
.metric-card{
    text-align:center;
    padding:1.5rem 1rem;
    border-radius:var(--radius);
    background:var(--glass);
    border:1px solid rgba(255,255,255,.06);
    transition:all .3s ease;
}
.metric-card:hover{
    border-color:var(--accent);
    transform:translateY(-4px);
}
.metric-value{
    font-size:2.5rem;
    font-weight:800;
    background:linear-gradient(90deg,var(--accent),var(--accent2));
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.metric-label{
    font-size:.875rem;
    color:var(--text2);
    margin-top:.25rem;
}

/* ---------- FOOTER ---------- */
footer{
    text-align:center;
    padding:3rem 0 2rem 0;
    font-size:.875rem;
    color:var(--text2);
    border-top:1px solid rgba(255,255,255,.06);
    margin-top:5rem;
}
</style>""",
    unsafe_allow_html=True,
)

# --------------  SIDEBAR GLASS STATS --------------
with st.sidebar:
    st.markdown("### 📊 Research Analytics")
    try:
        stats = MemoryBank().get_statistics()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{stats.get("total_memories",0)}</div><div class="metric-label">Total Research</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{stats.get("completed_sessions",0)}</div><div class="metric-label">Completed</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{stats.get("total_sources",0)}</div><div class="metric-label">Sources</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{stats.get("avg_importance",0):.1f}</div><div class="metric-label">Avg Quality</div></div>',
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

# --------------  FLOATING HERO  --------------
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
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-value">{summary.get("total_sources",0)}</div><div class="metric-label">Sources</div></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="metric-card"><div class="metric-value">{summary.get("iterations",0)}</div><div class="metric-label">Iterations</div></div>',
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-value">{validation.get("confidence_score",0)}%</div><div class="metric-label">Confidence</div></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="metric-card"><div class="metric-value">{output_format.title()}</div><div class="metric-label">Format</div></div>',
                    unsafe_allow_html=True,
                )

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
    '<footer><strong>AI Research Assistant
