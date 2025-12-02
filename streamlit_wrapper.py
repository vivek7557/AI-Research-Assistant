"""
CYBER•NEXUS v10 – MINIMALIST VERSION WITH REACT UI
Clean UI with gradient buttons and PDF export
"""

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import requests
import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator
from memory.memory_bank import MemoryBank

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Cyber Nexus",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# LOTTIE ANIMATION
# ======================================================
@st.cache_data(ttl=3600)
def load_lottie():
    try:
        with open("assets/lottie_brain.json", "r") as f:
            return json.load(f)
    except:
        try:
            r = requests.get("https://assets9.lottiefiles.com/packages/lf20_kkflmtur.json")
            if r.status_code == 200:
                return r.json()
        except:
            pass
    return None

lottie = load_lottie()

# ======================================================
# ENHANCED VISUAL CSS
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Main Background with Animated Gradient */
    .main { 
        background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #533483);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Title with Glow Effect */
    .big-title {
        font-size: 88px; 
        font-weight: 900; 
        text-align: center;
        background: linear-gradient(90deg, #a8edea, #fed6e3, #a8edea);
        background-size: 200% auto;
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        margin: 40px 0 10px; 
        letter-spacing: -3px;
        animation: shimmer 3s linear infinite;
        filter: drop-shadow(0 0 30px rgba(168, 237, 234, 0.5));
    }
    
    @keyframes shimmer {
        to { background-position: 200% center; }
    }
    
    /* Subtitle with Typing Effect */
    .subtitle { 
        text-align: center; 
        font-size: 24px; 
        color: rgba(255,255,255,0.9); 
        margin-bottom: 60px;
        font-weight: 300;
        letter-spacing: 2px;
    }
    
    /* Enhanced Glass Effect */
    .glass {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(30px);
        border-radius: 32px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 40px; 
        margin: 20px 0;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .glass::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Input Fields */
    .stTextInput input {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 16px !important;
        color: white !important;
        font-size: 16px !important;
        padding: 16px 20px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus {
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(168, 237, 234, 0.5) !important;
        box-shadow: 0 0 20px rgba(168, 237, 234, 0.2) !important;
    }
    
    /* Slider Enhancement */
    .stSlider {
        padding: 20px 0;
    }
    
    /* Button Styles with Gradient */
    .stButton button {
        border-radius: 16px !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        border: none !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3) !important;
    }
    
    /* Primary Button Gradient */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb) !important;
        background-size: 200% 100% !important;
        animation: progressGlow 2s ease infinite !important;
    }
    
    @keyframes progressGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Tabs Enhancement */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 14px;
        color: rgba(255,255,255,0.7);
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 16px !important;
        color: white !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        color: rgba(255,255,255,0.9) !important;
        font-weight: 600 !important;
    }
    
    /* Success/Warning Messages */
    .stSuccess, .stWarning {
        border-radius: 16px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Iframe for React Component */
    iframe {
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2, #667eea);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="big-title">Cyber Nexus</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Autonomous Research Intelligence • 2025</p>', unsafe_allow_html=True)

if lottie:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st_lottie(lottie, height=300, key="brain")

add_vertical_space(3)

# ======================================================
# INPUT SECTION
# ======================================================
with st.container():
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    colored_header("Begin Your Research", "Ask anything – get deep, verified answers", "violet-70")

    query = st.text_input(
        "What do you want to know?",
        placeholder="e.g. Neuralink 2025, AGI timelines, fusion breakthrough...",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        depth_level = st.slider("Research Depth", 1, 5, 3)
    with col2:
        st.write(""); st.write("")
        start_research = st.button("Start Research", type="primary", use_container_width=True)
    with col3:
        st.write(""); st.write("")
        clear_btn = st.button("Clear", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Clear functionality
if clear_btn:
    st.rerun()

# API key check
if not (st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")) or \
   not (st.secrets.get("TAVILY_API_KEY") or os.getenv("TAVILY_API_KEY")):
    st.error("Missing API keys. Add to Streamlit Secrets or .env")
    st.stop()

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3 = st.tabs(["RESEARCH", "MEMORY", "ARCHIVE"])

# ======================================================
# RESEARCH TAB
# ======================================================
with tab1:
    with st.container():
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        col1, col2 = st.columns([3,2])
        with col1:
            output_format = st.selectbox("Output Format", ["report", "article", "summary", "presentation", "paper"])

        with st.expander("Advanced Options"):
            session_id = st.text_input("Resume Session ID (optional)")

        st.markdown("</div>", unsafe_allow_html=True)

    # Trigger research
    if start_research:
        if not query.strip():
            st.warning("Please enter a query")
            st.stop()

        with st.spinner("Deploying neural agents..."):
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                time.sleep(0.03)
                progress_bar.progress(i + 1)
                status_text.caption(f"Researching... {i+1}%")

            results = ResearchOrchestrator().conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id or None
            )

        st.success("Research Complete")
        st.balloons()

        content = results.get("final_content", {}).get("content", "")

        # Result
        colored_header(f"Result: {query}", "", "blue-70")
        st.markdown(f"<div class='glass'>{content}</div>", unsafe_allow_html=True)

        # React UI with Gradient Buttons
        st.write("")
        st.markdown("### Download Options")
        
        # Prepare data for React component
        react_data = {
            "query": query,
            "content": content,
            "results": results
        }
        
        # React Component with Gradient Buttons
        html_component = f"""
        <div id="root"></div>
        <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        
        <script>
        const {{ useState }} = React;
        const data = {json.dumps(react_data)};
        
        function GradientDownloadButtons() {{
            const [hoveredBtn, setHoveredBtn] = useState(null);
            
            const downloadJSON = () => {{
                const blob = new Blob([JSON.stringify(data.results, null, 2)], {{ type: 'application/json' }});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'result.json';
                a.click();
            }};
            
            const downloadText = () => {{
                const blob = new Blob([data.content], {{ type: 'text/plain' }});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'report.txt';
                a.click();
            }};
            
            const downloadPDF = () => {{
                const {{ jsPDF }} = window.jspdf;
                const doc = new jsPDF();
                
                doc.setFontSize(20);
                doc.text(data.query, 20, 20);
                
                doc.setFontSize(12);
                const lines = doc.splitTextToSize(data.content, 170);
                doc.text(lines, 20, 40);
                
                doc.save('report.pdf');
            }};
            
            const buttons = [
                {{
                    label: 'JSON',
                    onClick: downloadJSON,
                    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    hoverGradient: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
                    icon: '📦'
                }},
                {{
                    label: 'Text',
                    onClick: downloadText,
                    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                    hoverGradient: 'linear-gradient(135deg, #f5576c 0%, #f093fb 100%)',
                    icon: '📝'
                }},
                {{
                    label: 'PDF',
                    onClick: downloadPDF,
                    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                    hoverGradient: 'linear-gradient(135deg, #fee140 0%, #fa709a 100%)',
                    icon: '📄'
                }}
            ];
            
            return React.createElement('div', {{
                style: {{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(3, 1fr)',
                    gap: '16px',
                    marginTop: '20px'
                }}
            }},
                buttons.map((btn, idx) => 
                    React.createElement('button', {{
                        key: idx,
                        onMouseEnter: () => setHoveredBtn(idx),
                        onMouseLeave: () => setHoveredBtn(null),
                        onClick: btn.onClick,
                        style: {{
                            background: hoveredBtn === idx ? btn.hoverGradient : btn.gradient,
                            border: 'none',
                            borderRadius: '12px',
                            padding: '20px 16px',
                            color: 'white',
                            fontSize: '15px',
                            fontWeight: '600',
                            cursor: 'pointer',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            gap: '8px',
                            transition: 'all 0.3s ease',
                            transform: hoveredBtn === idx ? 'translateY(-3px)' : 'translateY(0)',
                            boxShadow: hoveredBtn === idx 
                                ? '0 12px 30px rgba(0,0,0,0.3)' 
                                : '0 6px 15px rgba(0,0,0,0.2)',
                            fontFamily: 'Inter, sans-serif',
                            letterSpacing: '0.5px'
                        }}
                    }},
                        React.createElement('span', {{ style: {{ fontSize: '24px' }} }}, btn.icon),
                        React.createElement('span', null, btn.label)
                    )
                )
            );
        }}
        
        ReactDOM.render(
            React.createElement(GradientDownloadButtons),
            document.getElementById('root')
        );
        </script>
        
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        </style>
        """
        
        st.components.v1.html(html_component, height=150)

# ======================================================
# MEMORY & ARCHIVE TABS
# ======================================================
with tab2:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    colored_header("Memory Bank", "Search past research", "blue-70")
    
    col1, col2 = st.columns([4,1])
    with col1:
        q = st.text_input("Search memory", label_visibility="collapsed", placeholder="Search memory...")
    with col2:
        st.write("")
        search_btn = st.button("Search", use_container_width=True)
    
    if search_btn and q:
        links = MemoryBank().get_related_research(q, limit=10)
        for item in links or []:
            with st.expander(item.get("query", "Untitled")):
                st.json(item)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    colored_header("Archive", "Previous sessions", "green-70")
    out = Path("outputs")
    if out.exists():
        for f in sorted(out.glob("*.json"), key=os.path.getmtime, reverse=True)[:20]:
            try:
                data = json.load(open(f))
                with st.expander(data.get("query", "Untitled")):
                    st.json(data)
            except:
                pass
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div style='text-align:center;padding:100px;color:rgba(255,255,255,0.7);font-size:18px;'>Cyber Nexus v10 – Built for the Future • 2025</div>", unsafe_allow_html=True)
