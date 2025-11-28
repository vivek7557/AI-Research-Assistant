import streamlit as st
import json
import requests
from orchestrator import ResearchOrchestrator

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔍 AI Research Assistant")


# =====================================================
# INPUTS
# =====================================================
query = st.text_input("Enter research topic", placeholder="e.g., Impact of AI on healthcare")

col1, col2 = st.columns(2)
output_format = col1.selectbox(
    "Output Format",
    ["report", "article", "summary", "presentation", "brochure"]
)
depth = col2.slider("Research Depth", 1, 5, 3)


# =====================================================
# RUN BUTTON
# =====================================================
if st.button("🚀 Start Research"):
    if not query.strip():
        st.warning("Please enter a query.")
        st.stop()

    orchestrator = ResearchOrchestrator()

    st.info("Running research...")
    results = orchestrator.conduct_research(
        query=query,
        output_format=output_format,
        depth=depth
    )

    # Store content for downloads
    content = results["final_content"]["content"]

    st.success("Research Completed!")

    # =====================================================
    # SHOW CONTENT
    # =====================================================
    st.markdown("### 📄 Research Output")
    st.markdown(content)

    # =====================================================
    # DOWNLOADS
    # =====================================================
    colA, colB, colC = st.columns(3)
    colA.download_button("📥 Markdown", data=content, file_name="research.md")
    colB.download_button("📥 JSON", data=json.dumps(results, indent=2), file_name="research.json")
    colC.download_button("📥 Text", data=content, file_name="research.txt")

    # =====================================================
    # BROCHURE PDF DOWNLOAD (ONLY IF AVAILABLE)
    # =====================================================
    if results.get("brochure"):
        st.markdown("### 📄 Brochure")
        st.download_button(
            "📥 Download Brochure PDF",
            data=results["brochure"]["pdf_bytes"],
            file_name="brochure.pdf",
            mime="application/pdf"
        )

    # =====================================================
    # TIMELINE (UI)
    # =====================================================
    st.markdown("### ⏱ Research Timeline")
    for step in results["timeline"]:
        st.markdown(f"**➡ {step['stage']}** — {step['timestamp']}")


# =====================================================
# CHATBOT (Groq Llama3)
# =====================================================
st.markdown("---")
st.markdown("## 💬 Ask Follow-up Questions")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_msg = st.text_input("Ask something:", key="chat_input")

if user_msg:
    st.session_state.chat_history.append({"role": "user", "content": user_msg})

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"},
        json={
            "model": "llama-3.1-8b-instant",   # NOT DEPRECATED
            "messages": st.session_state.chat_history
        }
    )

    ai_reply = r.json()["choices"][0]["message"]["content"]
    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})


# =====================================================
# RENDER CHAT MESSAGES
# =====================================================
chat_style = """
<style>
.chat-user {
    background:#1e293b;
    padding:8px 12px;
    margin:6px 0;
    border-radius:8px;
    color:white;
}
.chat-ai {
    background:#334155;
    padding:8px 12px;
    margin:6px 0;
    border-radius:8px;
    color:#d1d5db;
}
</style>
"""
st.markdown(chat_style, unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-ai'>{msg['content']}</div>", unsafe_allow_html=True)
