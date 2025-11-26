import streamlit as st
import json
from orchestrator import ResearchOrchestrator
from evaluation.evaluator import ResearchEvaluator
from ui.theme import load_theme
load_theme()

# ============================
# Inject CSS for evaluation UI
# ============================
EVAL_CSS = """
<style>
.eval-row {
    display: flex;
    align-items: center;
    margin: 8px 0px;
    padding: 6px 0px;
}

.eval-label {
    width: 140px;
    font-weight: 600;
    font-size: 0.92rem;
    color: #e2e8f0;
}

.eval-bar {
    flex-grow: 1;
    height: 10px;
    background: #1e293b;
    border-radius: 6px;
    margin: 0 12px;
    overflow: hidden;
}

.eval-fill {
    height: 100%;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    border-radius: 6px;
}

.eval-score {
    width: 55px;
    text-align: right;
    font-weight: 700;
    font-size: 0.95rem;
    color: #e2e8f0;
}

.eval-explain {
    margin-top: 4px;
    font-size: 0.8rem;
    color: #94a3b8;
}
</style>
"""
st.markdown(EVAL_CSS, unsafe_allow_html=True)


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

        # =============================
        # QUALITY EVALUATION SECTION
        # =============================
        if run_eval:
            st.markdown("---")
            st.markdown("<h2>📊 Quality Evaluation</h2>", unsafe_allow_html=True)

            evaluator = ResearchEvaluator()
            metrics = evaluator.evaluate_research(query, results).to_dict()

            explanations = {
                "completeness": "Checks how well the research covers all required aspects of the topic.",
                "accuracy": "Measures factual correctness based on known verified sources.",
                "relevance": "Evaluates if the content stays focused on the main research question.",
                "quality": "Assesses writing clarity, structure, and depth.",
                "efficiency": "Judges how effectively sources were used.",
                "citations": "Checks if proper citations were included.",
                "overall": "Weighted average of all metrics — overall quality score."
            }

            for metric, score in metrics.items():
                st.markdown(metric_bar(metric, score), unsafe_allow_html=True)
                st.markdown(
                    f"<div class='eval-explain'>{explanations.get(metric, '')}</div>",
                    unsafe_allow_html=True
                )


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
