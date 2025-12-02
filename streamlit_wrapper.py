# ======================================================
#  NEW – STREAMLIT-NATIVE UI  (replaces everything above)
# ======================================================
st.set_page_config(
    page_title="Cyber Nexus",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------  CSS (same dark vibe, no JS)  -------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.main {
    background: #0a0a0a;
    font-family: 'Inter', sans-serif;
}

.glass {
    background: #141414;
    border-radius: 24px;
    border: 1px solid #222222;
    padding: 40px;
    margin: 20px 0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}

.big-title {
    font-size: 88px;
    font-weight: 900;
    text-align: center;
    color: #ffffff;
    margin: 40px 0 10px;
    letter-spacing: -3px;
}

.subtitle {
    text-align: center;
    font-size: 24px;
    color: #888888;
    margin-bottom: 60px;
    font-weight: 400;
    letter-spacing: 0.5px;
}

.stButton button {
    border-radius: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
    transition: all 0.2s ease;
    border: none;
    padding: 12px 28px;
    font-size: 15px;
}

.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}

.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #ff4757 0%, #ff6b7a 100%) !important;
    color: white !important;
}

.stButton button[kind="primary"]:hover {
    background: linear-gradient(135deg, #ff6b7a 0%, #ff4757 100%) !important;
}

.stTextInput input, .stTextArea textarea {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 16px !important;
    padding: 14px 18px !important;
}

.stSlider > div > div > div > div {
    background: #ff4757 !important;
}

.stTabs [aria-selected="true"] {
    color: #ff4757 !important;
    border-bottom: 2px solid #ff4757 !important;
}
</style>
""", unsafe_allow_html=True)

# ----------  HEADER  ----------
st.markdown('<h1 class="big-title">Cyber Nexus</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Autonomous Research Intelligence • 2025</p>', unsafe_allow_html=True)

# ----------  INPUT  ----------
with st.container():
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    query = st.text_input(
        "What do you want to know?",
        placeholder="e.g. Neuralink 2025, AGI timelines, fusion breakthrough..."
    )

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        depth_level = st.slider("Research Depth", 1, 5, 3)
    with c2:
        start_research = st.button("Start Research", type="primary", use_container_width=True)
    with c3:
        if st.button("Clear", use_container_width=True):
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ----------  API KEY GUARD  -------------
if not (st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")) or \
   not (st.secrets.get("TAVILY_API_KEY") or os.getenv("TAVILY_API_KEY")):
    st.error("Missing API keys. Add to Streamlit Secrets or .env")
    st.stop()

# ----------  TABS  ----------
tab1, tab2, tab3 = st.tabs(["RESEARCH", "MEMORY", "ARCHIVE"])

# ----------  RESEARCH  ----------
with tab1:
    with st.container():
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        output_format = st.selectbox("Output Format", ["report", "article", "summary", "presentation", "paper"])
        session_id = st.text_input("Resume Session ID (optional)")
        st.markdown("</div>", unsafe_allow_html=True)

    if start_research and query.strip():
        with st.spinner("Deploying neural agents..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.03)
                progress.progress(i + 1)

            results = ResearchOrchestrator().conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id or None
            )
            progress.empty()

        st.success("Research Complete")
        st.balloons()

        content = results.get("final_content", {}).get("content", "")
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown(content)
        st.markdown("</div>", unsafe_allow_html=True)

        # ----  simple download row  ----
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.download_button("📋 Copy", data=content, file_name=None, mime="text/plain")
        with col_b:
            st.download_button("💾 JSON", data=json.dumps(results, indent=2), file_name="research.json", mime="application/json")
        with col_c:
            st.download_button("📝 TXT", data=content, file_name="research.txt", mime="text/plain")
        with col_d:
            # basic PDF (utf-8 text only)
            try:
                from fpdf import FPDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=11)
                for line in content.split("\n"):
                    pdf.multi_cell(0, 5, line.encode("latin-1", "replace").decode("latin-1"))
                st.download_button("📄 PDF", data=pdf.output(dest="S"), file_name="research.pdf", mime="application/pdf")
            except Exception:
                st.download_button("📄 PDF", data=content, file_name="research.txt", mime="text/plain")

# ----------  MEMORY  ----------
with tab2:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    q = st.text_input("Search memory", placeholder="Search memory...")
    if st.button("Search") and q:
        links = MemoryBank().get_related_research(q, limit=10)
        for item in links or []:
            with st.expander(item.get("query", "Untitled")):
                st.json(item)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------  ARCHIVE  ----------
with tab3:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    out = Path("outputs")
    if out.exists():
        for f in sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)[:20]:
            try:
                data = json.load(open(f))
                with st.expander(data.get("query", "Untitled")):
                    st.json(data)
            except Exception:
                pass
    st.markdown("</div>", unsafe_allow_html=True)

# ----------  FOOTER  ----------
st.markdown("<div style='text-align:center;padding:100px;color:rgba(255,255,255,0.7);font-size:18px;'>Cyber Nexus v10 – Built for the Future • 2025</div>", unsafe_allow_html=True)
