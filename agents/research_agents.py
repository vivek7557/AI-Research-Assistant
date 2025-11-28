import json
import time
from loguru import logger
from agents.llm_model import run_llm

# ===================================================================
# 1. QUERY PLANNER AGENT
# ===================================================================
class QueryPlannerAgent:

    def plan_research(self, query: str, session_id: str):
        system_prompt = (
            "You are a research planning agent. "
            "Return ONLY valid JSON with key 'sub_questions'."
        )

        user_prompt = f"""
Create a research plan for: "{query}"

Return JSON exactly like this:

{{
    "sub_questions": [
        "Question 1",
        "Question 2",
        "Question 3"
    ]
}}
"""

        llm_output = run_llm(system_prompt, user_prompt)
        logger.info("Planner LLM raw output:")
        logger.info(llm_output)

        try:
            plan = json.loads(llm_output)
        except Exception:
            logger.error("[Planner Error] Invalid JSON received.")
            try:
                start = llm_output.index("{")
                end = llm_output.rindex("}") + 1
                json_chunk = llm_output[start:end]
                plan = json.loads(json_chunk)
            except Exception:
                logger.warning("[Planner] JSON repair failed → using fallback")
                plan = {
                    "sub_questions": [
                        f"What is the overview of {query}?",
                        f"What are the latest developments in {query}?",
                        f"What challenges exist in {query}?"
                    ]
                }

        if not isinstance(plan, dict):
            plan = {}

        if "sub_questions" not in plan or not isinstance(plan["sub_questions"], list):
            plan["sub_questions"] = [
                f"Overview of {query}",
                f"Recent trends in {query}",
                f"Challenges in {query}"
            ]

        return plan


# ===================================================================
# 2. RESEARCH AGENT
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

        iterations = loop_iterations or self.iterations
        collected_sources = []

        for i in range(iterations):
            for q in sub_questions:

                # -------------------------------
                # SAFE SEARCH CALL (NO CRASHING)
                # -------------------------------
                try:
                    res = self.search_tool.search(
                        q,
                        max_results=self.sources_per_iter
                    )
                except Exception as e:
                    # if Tavily or internet fails → skip safely
                    logger.error(f"[Search Error] {e}")
                    res = None

                # -------------------------------
                # ALWAYS SAFE → extract list
                # -------------------------------
                if res and isinstance(res, dict):
                    sources = res.get("results", [])
                    if not isinstance(sources, list):
                        sources = []
                else:
                    sources = []

                # always extend list
                collected_sources.extend(sources)

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

        # ---- SAFETY FIX ----
        if not sources or not isinstance(sources, list):
            sources = []

        extracted_info = "\n".join(
            [(s.get("content") or "")[:500] for s in sources[:10]]
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
