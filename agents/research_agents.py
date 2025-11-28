import json
import time
from loguru import logger
from agents.llm_model import run_llm


# ===================================================================
# 1. QUERY PLANNER AGENT
# ===================================================================
class QueryPlannerAgent:

    def plan_research(self, query: str, session_id: str):
        """
        Generates sub-questions for the research workflow.
        Ensures JSON output. Repairs invalid JSON automatically.
        """

        system_prompt = "You are a research planning agent. Output ONLY valid JSON."

        user_prompt = f"""
Create a research plan for: {query}

Return JSON EXACTLY like:
{
    "sub_questions": [
        "Question 1",
        "Question 2",
        "Question 3"
    ]
}
"""

        llm_output = run_llm(system_prompt, user_prompt)

        # Attempt JSON parsing
        try:
            plan = json.loads(llm_output)

        except Exception:
            logger.error(f"[Planner Error] Invalid JSON: {llm_output}")

            # Try soft repair
            try:
                start = llm_output.index("{")
                end = llm_output.rindex("}") + 1
                plan = json.loads(llm_output[start:end])
            except Exception:
                # Hard fallback
                plan = {
                    "sub_questions": [
                        f"What is the overview of {query}?",
                        f"What are current developments in {query}?",
                        f"What challenges exist in {query}?"
                    ]
                }

        # Final safety validation
        if "sub_questions" not in plan:
            plan["sub_questions"] = [
                f"Overview of {query}",
                f"Recent trends in {query}",
                f"Challenges in {query}"
            ]

        return plan


# ===================================================================
# 2. RESEARCH AGENT (SEARCH + LOOP)
# ===================================================================
class ResearchAgent:

    def __init__(self, search_tool):
        self.search_tool = search_tool
        self.iterations = 3
        self.sources_per_iter = 5

    def set_depth(self, iterations, sources):
        self.iterations = iterations
        self.sources_per_iter = sources

    def research(self, sub_questions, session_id, memory_bank, loop_iterations=None):

        if loop_iterations:
            iterations = loop_iterations
        else:
            iterations = self.iterations

        collected_sources = []

        for i in range(iterations):
            for q in sub_questions:
                res = self.search_tool.search(q, top_k=self.sources_per_iter)
                collected_sources.extend(res)

            time.sleep(0.2)

        return {
            "sources": collected_sources,
            "total_sources": len(collected_sources),
            "iterations_completed": iterations
        }


# ===================================================================
# 3. SYNTHESIS AGENT
# ===================================================================
class SynthesisAgent:

    def synthesize(self, sources, query, session_id):

        extracted_info = "\n".join(
            [s.get("content", "")[:500] for s in sources[:10]]
        )

        system = "You are a synthesis agent. Summarize research findings."
        user = f"""
Combine and synthesize the following research results for: {query}

Sources:
{extracted_info}

Write a well-structured synthesis.
"""

        synthesis_text = run_llm(system, user)

        return {"synthesis": synthesis_text}


# ===================================================================
# 4. VALIDATION AGENT
# ===================================================================
class ValidationAgent:

    def validate(self, synthesis_text, sources, session_id):

        system = "You are a validation agent. Detect gaps or contradictions."
        user = f"""
Validate the following synthesized research:

{synthesis_text}

Check for:
- Missing information
- Contradictions
- Logical gaps

Return a helpful validation report.
"""

        validation_text = run_llm(system, user)

        return {"validation": validation_text}


# ===================================================================
# 5. CONTENT GENERATOR AGENT
# ===================================================================
class ContentGeneratorAgent:

    def generate(self, synthesis_text, validation_results, sources, output_format, session_id):

        source_list = "\n".join([f"- {s.get('url', '')}" for s in sources[:10]])

        system = "You are an expert content generator."
        user = f"""
Write a {output_format} based on this synthesis:

{synthesis_text}

Validation notes:
{validation_results}

Include a short conclusion.

Sources:
{source_list}
"""

        final = run_llm(system, user)

        return {
            "content": final,
            "word_count": len(final.split())
        }
