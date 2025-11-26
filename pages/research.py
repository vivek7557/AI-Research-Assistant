import streamlit as st
import json
from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator
from ui.theme import load_theme
load_theme()


def research_page():
    st.markdown("<h1 class='page-title'>New Research</h1>", unsafe_allow_html=True)

    query = st.text_input("Enter research topic", placeholder="e.g., Impact of AI on healthcare")

    col1, col2 = st.columns(2)
    output_format = col1.selectbox("Output Format", ["report", "article", "summary", "presentation"])
    run_eval = col2.checkbox("Run Evaluation", value=True)

    with st.expander("Advanced Options"):
        colA, colB = st.columns(2)
        session_id = colA.text_input("Resume session", placeholder="session_xxx")
        depth = colB.slider("Depth", 1, 5, 3)

    if st.button("🚀 Run Research"):
        if not query.strip():
            st.warning("Please enter a valid query.")
            return

        orchestrator = ResearchOrchestrator()

        with st.spinner("Running agents..."):
            results = orchestrator.conduct_research(
                query=query,
                output_format=output_format,
                session_id=session_id or None,
                depth=depth
            )

        st.success("Research completed!")
        content = results["final_content"]["content"]
        st.markdown(content)

        # Downloads
        col1, col2, col3 = st.columns(3)
        col1.download_button("📥 Markdown", content, "research.md")
        col2.download_button("📥 JSON", json.dumps(results, indent=2), "research.json")
        col3.download_button("📥 Text", content, "research.txt")

        # Evaluation
        if run_eval:
            st.markdown("---")
            st.markdown("<h3>Quality Evaluation</h3>", unsafe_allow_html=True)
            evaluator = ResearchEvaluator()
            metrics = evaluator.evaluate_research(query, results).to_dict()

            for m, score in metrics.items():
                st.markdown(metric_bar(m, score))

def metric_bar(name, score):
    label = name.replace("_", " ").title()
    return f"""
    <div class='eval-row'>
        <div class='eval-label'>{label}</div>
        <div class='eval-bar'>
            <div class='eval-fill' style='width:{score}%;'></div>
        </div>
        <div class='eval-score'>{score}</div>
    </div>
    """

