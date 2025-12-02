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
# MODERN DARK UI CSS
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Dark Modern Background */
    .main { 
        background: #0a0a0a;
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern Title */
    .big-title {
        font-size: 88px; 
        font-weight: 900; 
        text-align: center;
        color: #ffffff;
        margin: 40px 0 10px; 
        letter-spacing: -3px;
    }
    
    /* Subtitle */
    .subtitle { 
        text-align: center; 
        font-size: 24px; 
        color: #888888; 
        margin-bottom: 60px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    /* Modern Card/Glass Effect */
    .glass {
        background: #141414;
        border-radius: 24px;
        border: 1px solid #222222;
        padding: 40px; 
        margin: 20px 0;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    }
    
    /* Input Fields - Modern Dark */
    .stTextInput input {
        background: #1a1a1a !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-size: 16px !important;
        padding: 14px 18px !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput input:focus {
        background: #222222 !important;
        border: 1px solid #3a3a3a !important;
        box-shadow: 0 0 0 3px rgba(255,255,255,0.05) !important;
    }
    
    .stTextInput input::placeholder {
        color: #666666 !important;
    }
    
    /* Slider - Modern Style */
    .stSlider {
        padding: 20px 0;
    }
    
    .stSlider > div > div > div > div {
        background: #ff4757 !important;
    }
    
    .stSlider > div > div > div {
        background: #2a2a2a !important;
    }
    
    /* Modern Buttons */
    .stButton button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        transition: all 0.2s ease !important;
        border: none !important;
        padding: 12px 28px !important;
        font-size: 15px !important;
    }
    
    .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3) !important;
    }
    
    /* Primary Button - Red Accent */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #ff4757 0%, #ff6b7a 100%) !important;
        color: white !important;
    }
    
    .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #ff6b7a 0%, #ff4757 100%) !important;
    }
    
    /* Secondary/Clear Button */
    .stButton button[kind="secondary"], 
    .stButton button:not([kind="primary"]) {
        background: transparent !important;
        border: 1px solid #2a2a2a !important;
        color: #ffffff !important;
    }
    
    .stButton button[kind="secondary"]:hover,
    .stButton button:not([kind="primary"]):hover {
        background: #1a1a1a !important;
        border: 1px solid #3a3a3a !important;
    }
    
    /* Progress Bar - Modern */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 4px !important;
    }
    
    .stProgress > div {
        background: #1a1a1a !important;
        border-radius: 4px !important;
    }
    
    /* Tabs - Modern Dark */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
        border-bottom: 1px solid #222222;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0;
        color: #666666;
        font-weight: 600;
        padding: 12px 24px;
        border: none;
        background: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #ff4757 !important;
        border-bottom: 2px solid #ff4757 !important;
    }
    
    /* Select Box - Modern */
    .stSelectbox > div > div {
        background: #1a1a1a !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    .stSelectbox svg {
        fill: #666666 !important;
    }
    
    /* Expander - Modern Dark */
    .streamlit-expanderHeader {
        background: #1a1a1a !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 14px 18px !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #222222 !important;
    }
    
    .streamlit-expanderContent {
        background: #141414 !important;
        border: 1px solid #2a2a2a !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* Success/Warning Messages */
    .stSuccess {
        background: #1a2f1a !important;
        border: 1px solid #2d4a2d !important;
        border-radius: 12px !important;
        color: #7ed87e !important;
    }
    
    .stWarning {
        background: #2f2a1a !important;
        border: 1px solid #4a432d !important;
        border-radius: 12px !important;
        color: #d8c77e !important;
    }
    
    .stError {
        background: #2f1a1a !important;
        border: 1px solid #4a2d2d !important;
        border-radius: 12px !important;
        color: #d87e7e !important;
    }
    
    /* Iframe for React Component */
    iframe {
        border-radius: 12px;
        border: 1px solid #222222;
    }
    
    /* Modern Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2a2a2a;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3a3a3a;
    }
    
    /* Labels and Text */
    label, .stMarkdown {
        color: #cccccc !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Caption text */
    .stCaption {
        color: #888888 !important;
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

        # Modern React UI with Gradient Cards
        st.write("")
        
        # Prepare data for React component
        react_data = {
            "query": query,
            "content": content,
            "results": results
        }
        
        # Enhanced React Component with Modern UI
        html_component = f"""
        <div id="root"></div>
        <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        
        <script>
        const {{ useState, useEffect }} = React;
        const data = {json.dumps(react_data)};
        
        function ModernDownloadUI() {{
            const [hoveredBtn, setHoveredBtn] = useState(null);
            const [copied, setCopied] = useState(false);
            const [downloading, setDownloading] = useState(null);
            
            const downloadJSON = () => {{
                setDownloading('json');
                setTimeout(() => {{
                    const blob = new Blob([JSON.stringify(data.results, null, 2)], {{ type: 'application/json' }});
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'research_result.json';
                    a.click();
                    setDownloading(null);
                }}, 500);
            }};
            
            const downloadText = () => {{
                setDownloading('text');
                setTimeout(() => {{
                    const blob = new Blob([data.content], {{ type: 'text/plain' }});
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'research_report.txt';
                    a.click();
                    setDownloading(null);
                }}, 500);
            }};
            
            const downloadPDF = () => {{
                setDownloading('pdf');
                setTimeout(() => {{
                    const {{ jsPDF }} = window.jspdf;
                    const doc = new jsPDF();
                    
                    doc.setFontSize(22);
                    doc.setFont(undefined, 'bold');
                    doc.text(data.query, 20, 25);
                    
                    doc.setFontSize(11);
                    doc.setFont(undefined, 'normal');
                    const lines = doc.splitTextToSize(data.content, 170);
                    doc.text(lines, 20, 45);
                    
                    doc.save('research_report.pdf');
                    setDownloading(null);
                }}, 500);
            }};
            
            const copyToClipboard = () => {{
                navigator.clipboard.writeText(data.content);
                setCopied(true);
                setTimeout(() => setCopied(false), 2000);
            }};
            
            const downloadOptions = [
                {{
                    id: 'json',
                    title: 'Export JSON',
                    description: 'Complete data structure',
                    onClick: downloadJSON,
                    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    icon: '{{ }}',
                    size: '24px'
                }},
                {{
                    id: 'text',
                    title: 'Save as Text',
                    description: 'Plain text format',
                    onClick: downloadText,
                    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                    icon: 'TXT',
                    size: '18px'
                }},
                {{
                    id: 'pdf',
                    title: 'Generate PDF',
                    description: 'Formatted document',
                    onClick: downloadPDF,
                    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                    icon: 'PDF',
                    size: '18px'
                }}
            ];
            
            return React.createElement('div', {{
                style: {{
                    background: '#0a0a0a',
                    padding: '40px 0',
                    fontFamily: 'Inter, -apple-system, sans-serif'
                }}
            }},
                // Header Section
                React.createElement('div', {{
                    style: {{
                        marginBottom: '32px',
                        textAlign: 'center'
                    }}
                }},
                    React.createElement('h2', {{
                        style: {{
                            fontSize: '32px',
                            fontWeight: '700',
                            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            marginBottom: '8px'
                        }}
                    }}, 'Export Research'),
                    React.createElement('p', {{
                        style: {{
                            fontSize: '15px',
                            color: '#888888',
                            fontWeight: '400'
                        }}
                    }}, 'Choose your preferred format')
                ),
                
                // Download Cards Grid
                React.createElement('div', {{
                    style: {{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                        gap: '20px',
                        marginBottom: '32px'
                    }}
                }},
                    downloadOptions.map((option, idx) => 
                        React.createElement('div', {{
                            key: option.id,
                            onMouseEnter: () => setHoveredBtn(option.id),
                            onMouseLeave: () => setHoveredBtn(null),
                            onClick: option.onClick,
                            style: {{
                                background: hoveredBtn === option.id 
                                    ? 'linear-gradient(135deg, #1a1a1a 0%, #222222 100%)'
                                    : '#141414',
                                border: hoveredBtn === option.id ? '1px solid #333333' : '1px solid #222222',
                                borderRadius: '16px',
                                padding: '28px 24px',
                                cursor: 'pointer',
                                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                                transform: hoveredBtn === option.id ? 'translateY(-4px)' : 'translateY(0)',
                                boxShadow: hoveredBtn === option.id 
                                    ? '0 20px 40px rgba(0,0,0,0.4)' 
                                    : '0 4px 12px rgba(0,0,0,0.2)',
                                position: 'relative',
                                overflow: 'hidden'
                            }}
                        }},
                            // Gradient overlay
                            React.createElement('div', {{
                                style: {{
                                    position: 'absolute',
                                    top: 0,
                                    left: 0,
                                    right: 0,
                                    height: '4px',
                                    background: option.gradient,
                                    opacity: hoveredBtn === option.id ? 1 : 0.6,
                                    transition: 'opacity 0.3s ease'
                                }}
                            }}),
                            
                            // Icon
                            React.createElement('div', {{
                                style: {{
                                    width: '56px',
                                    height: '56px',
                                    borderRadius: '12px',
                                    background: option.gradient,
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    marginBottom: '16px',
                                    fontSize: option.size,
                                    fontWeight: '800',
                                    color: 'white',
                                    boxShadow: hoveredBtn === option.id 
                                        ? '0 8px 24px rgba(0,0,0,0.3)' 
                                        : '0 4px 12px rgba(0,0,0,0.2)',
                                    transition: 'all 0.3s ease'
                                }}
                            }}, option.icon),
                            
                            // Title
                            React.createElement('h3', {{
                                style: {{
                                    fontSize: '18px',
                                    fontWeight: '600',
                                    color: '#ffffff',
                                    marginBottom: '6px'
                                }}
                            }}, option.title),
                            
                            // Description
                            React.createElement('p', {{
                                style: {{
                                    fontSize: '14px',
                                    color: '#888888',
                                    fontWeight: '400',
                                    marginBottom: '16px'
                                }}
                            }}, option.description),
                            
                            // Status
                            downloading === option.id && React.createElement('div', {{
                                style: {{
                                    fontSize: '13px',
                                    color: '#667eea',
                                    fontWeight: '500'
                                }}
                            }}, '⬇ Downloading...')
                        )
                    )
                ),
                
                // Quick Copy Button
                React.createElement('div', {{
                    style: {{
                        display: 'flex',
                        justifyContent: 'center'
                    }}
                }},
                    React.createElement('button', {{
                        onClick: copyToClipboard,
                        style: {{
                            background: copied ? '#1a2f1a' : 'transparent',
                            border: copied ? '1px solid #2d4a2d' : '1px solid #2a2a2a',
                            borderRadius: '12px',
                            padding: '14px 32px',
                            color: copied ? '#7ed87e' : '#ffffff',
                            fontSize: '14px',
                            fontWeight: '600',
                            cursor: 'pointer',
                            transition: 'all 0.3s ease',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px'
                        }}
                    }},
                        React.createElement('span', {{ style: {{ fontSize: '16px' }} }}, copied ? '✓' : '📋'),
                        React.createElement('span', null, copied ? 'Copied to Clipboard!' : 'Copy to Clipboard')
                    )
                )
            );
        }}
        
        ReactDOM.render(
            React.createElement(ModernDownloadUI),
            document.getElementById('root')
        );
        </script>
        
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        </style>
        """
        
        st.components.v1.html(html_component, height=520)

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
