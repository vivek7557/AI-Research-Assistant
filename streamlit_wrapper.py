import streamlit as st
import json
import time
import requests
from pathlib import Path

from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator


# -----------------------------------------------------------
# PAGE SETTINGS
# -----------------------------------------------------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Research Assistant")


# -----------------------------------------------------------
# INPUTS
# -----------------------------------------------------------
query = st.text_input("Enter research topic")
output_format = st.selectbox("Output Format", ["report", "article", "summary"])
depth = st.slider("Depth", 1, 5, 3)
run_eval = st.checkbox("Run Evaluation", True)

run = st.button("🚀 Run Research")


# ===========================================================
# RUN RESEARCH
# ===========================================================
if run:
    if not query.strip():
        st.error("Enter a query")
        st.stop()

    orchestrator = ResearchOrchestrator()

    st.info("Running research... please wait")
    results = orchestrator.conduct_research(
        query=query,
        output_format=output_format,
        depth=depth
    )

    st.success("Research Completed")


    # =======================================================
    # Show generated content
    # =======================================================
    content = results["final_content"]["content"]
    st.markdown("### 📄 Generated Content")
    st.markdown(content)


    # =======================================================
    # Downloads
    # =======================================================
    st.markdown("---")
    d1, d2, d3 = st.columns(3)

    d1.download_button("📥 Markdown", data=content, file_name="research.md")
    d2.download_button("📥 JSON", data=json.dumps(results, indent=2), file_name="research.json")
    d3.download_button("📥 Text", data=content, file_name="research.txt")


    # =======================================================
    # Brochure PDF
    # =======================================================
    if results.get("brochure"):
        st.markdown("### 📄 Brochure PDF")
        st.download_button(
            "📥 Download Brochure PDF",
            data=results["brochure"]["pdf_bytes"],
            file_name="brochure.pdf",
            mime="application/pdf"
        )


    # =======================================================
    # Evaluation
    # =======================================================
    if run_eval:
        st.markdown("---")
        st.markdown("### 📊 Evaluation")

        evaluator = ResearchEvaluator()
        metrics = evaluator.evaluate_research(query, results).to_dict()

        for m, score in metrics.items():
            label = m.replace("_", " ").title()
            st.write(f"**{label}:** {score}")


    # =======================================================
    # Show citations
    # =======================================================
    st.markdown("---")
    st.markdown("### 🔗 Citations / Sources")

    for s in results["sources"]:
        st.markdown(f"- [{s.get('title')}]({s.get('url', '')})")


# ===========================================================
# CHATBOT
# ===========================================================
st.markdown("---")
st.markdown("## 💬 Chat")

user_msg = st.text_input("Ask something")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if user_msg:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_msg}
    )

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"},
        json={
            "model": "mixtral-8x7b-32768",
            "messages": st.session_state.chat_history
        }
    )

    reply = r.json()["choices"][0]["message"]["content"]
    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply}
    )

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **AI:** {msg['content']}")
