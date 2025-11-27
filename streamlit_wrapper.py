import streamlit as st
import time
import uuid
import json
import requests
from pathlib import Path

from orchestrator import ResearchOrchestrator  # your existing file

# ==============================================================
# PAGE SETTINGS
# ==============================================================
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
)

# ==============================================================
# THEME & GLOBAL CSS
# ==============================================================
st.markdown("""
<style>

body, .stApp {
    background-color: #0d1117 !important;
}

/* Remove top padding */
.block-container {
    padding-top: 1rem !important;
    max-width: 1150px;
}

/* -------------------------
   BEAUTIFUL PAGE TITLE
-------------------------- */
.page-title {
    font-size: 2.3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* -------------------------
   FLOATING CHAT BUBBLE
-------------------------- */
.chat-bubble {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 62px;
    height: 62px;
    background: #6c47ff;
    border-radius: 50%;
    box-shadow: 0 6px 16px rgba(120,80,255,0.35);
    display:flex;
    align-items:center;
    justify-content:center;
    cursor:pointer;
    transition:0.2s;
}

.chat-bubble:hover {
    transform: scale(1.08);
}

/* Chat icon */
.chat-bubble-icon {
    font-size: 28px;
    color:white;
}

/* -----------------------------
   CHAT PANEL (SLIDE-IN)
------------------------------ */
#chat-panel {
    position: fixed;
    top: 0;
    right: -420px;
    width: 400px;
    height: 100vh;
    background: #111827;
    border-left: 1px solid #1f2937;
    padding: 20px;
    transition: right 0.35s ease;
    overflow-y:auto;
}

.chat-panel-open {
    right: 0 !important;
}

/* Chat message bubbles */
.chat-msg-user {
    background: #2563eb;
    color:white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom:8px;
    max-width:80%;
}

.chat-msg-ai {
    background: #374151;
    color:white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom:8px;
    max-width:80%;
}

/* Research Input Container */
.research-box {
    background:#111827;
    padding:20px;
    border-radius:12px;
    border:1px solid #1f2937;
    margin-top:10px;
}

</style>

<script>
// toggle chat panel
function toggleChat() {
    let panel=document.getElementById("chat-panel");
    panel.classList.toggle("chat-panel-open");
}
</script>
""", unsafe_allow_html=True)


# ==============================================================
# FLOATING CHAT BUBBLE HTML
# ==============================================================
st.markdown("""
<div class="chat-bubble" onclick="toggleChat()">
   <div class="chat-bubble-icon">💬</div>
</div>

<div id="chat-panel">
    <h3 style="color:white;">AI Chat Assistant</h3>
    <div id="chat-container"></div>
</div>
""", unsafe_allow_html=True)


# ==============================================================
# PAGE HEADER
# ==============================================================
st.markdown("<div class='page-title'>AI Research Assistant</div>", unsafe_allow_html=True)


# RESEARCH INPUT AREA
st.markdown("<h2 style='color:#e5e7eb;'>New Research</h2>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='research-box'>", unsafe_allow_html=True)

    query = st.text_input("Enter research topic:")
    col1, col2 = st.columns(2)
    output_format = col1.selectbox("Output Format", ["report","article","summary","presentation"])
    depth = col2.slider("Research Depth", 1, 5, 3)

    st.markdown("</div>", unsafe_allow_html=True)

run = st.button("🚀 Start Research", use_container_width=True)

if run:
    if not query.strip():
        st.warning("Enter a topic first.")
        st.stop()

    st.info("Running research...")
    orchestrator = ResearchOrchestrator()

    results = orchestrator.conduct_research(
        query=query,
        output_format=output_format,
        depth=depth
    )

    st.success("Research completed!")

    st.markdown("### 📄 Final Research")
    st.markdown(results["final_content"]["content"])

    # Citations
    st.markdown("### 🔗 Citations")
    for src in results["research_summary"].get("sources", []):
        st.markdown(f"- [{src.get('title','source')}]({src.get('url','')})")

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

# =============== BROCHURE DOWNLOAD ===============
if results.get("brochure"):
    st.markdown("### 📄 Brochure PDF")
    st.download_button(
        "📥 Download Brochure PDF",
        data=results["brochure"]["pdf_bytes"],
        file_name="brochure.pdf",
        mime="application/pdf"
    )


st.markdown("### ")

user_msg = st.text_input("Chat with AI:", key="chatbox")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if user_msg:
    st.session_state.chat_history.append({"role":"user","content":user_msg})

    # Call GROQ Mixtral
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization":f"Bearer {st.secrets['GROQ_API_KEY']}"},
        json={
            "model": "mixtral-8x7b-32768",
            "messages": st.session_state.chat_history
        }
    )

    ai_reply = r.json()["choices"][0]["message"]["content"]
    st.session_state.chat_history.append({"role":"assistant","content":ai_reply})

# Render chat
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-msg-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-msg-ai'>{msg['content']}</div>", unsafe_allow_html=True)

