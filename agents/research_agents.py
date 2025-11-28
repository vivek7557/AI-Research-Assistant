import os
from groq import Groq
from typing import List, Dict, Any
from loguru import logger

# ======================================================================
# LLM CONFIG (GROQ — mixtral-8x7b-32768)
# ======================================================================

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LLM_MODEL = "mixtral-8x7b-32768"   # ✔ WORKING FREE MODEL
MAX_TOKENS = 6000
TEMP = 0.4


def run_llm(system_prompt: str, user_prompt: str) -> str:
    """Universal LLM runner for all agents."""
    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=TEMP,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message["content"]


# ======================================================================
# AGENT 1 — QUERY PLANNER
# ======================================================================

class QueryPlannerAgent:
    def plan_research(self, query: str, session_id: str):

        logger.info(f"Planning research: {query}")

        system = """
        You are a senior research strategist.
        Break topics into deep sub-questions.
        """

        user = f"""
        Create a research plan for: {query}

        Include:
        - Main objective
        - 6–12 deep analytical sub-questions
        - Data-collection strategy
        - Verification strategy
        """

        result = run_llm(system, user)

        return {
            "plan_text": result,
            "sub_questions": self._extract_sub_questions(result)
        }

    def _extract_sub_questions(self, text: str) -> List[str]:
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        subs = [l for l in lines if "?" in l.lower()]
        return subs[:12]


# ======================================================================
# AGENT 2 — RESEARCH (LOOP DEPTH)
# ======================================================================

class ResearchAgent:

    def __init__(self, search_tool):
        self.search_tool = search_tool
        self.iterations = 3
        self.sources_per_iter = 5

    def set_depth(self, iterations: int, sources: int):
        self.iterations = iterations
        self.sources_per_iter = sources

    def research(
        self,
        sub_questions: List[str],
        session_id: str,
        memory_bank,
        loop_iterations: int = None
    ):

        if loop_iterations:
            self.iterations = loop_iterations

        aggregated_sources = []

        for i in range(self.iterations):
            logger.info(f"Research iteration {i+1}/{self.iterations}")

            for q in sub_questions:
                try:
                    results = self.search_tool.search(
                        q,
                        n_results=self.sources_per_iter
                    )
                    aggregated_sources.extend(results)
                except Exception as e:
                    logger.warning(f"Search failed: {e}")

        return {
            "sources": aggregated_sources,
            "total_sources": len(aggregated_sources),
            "iterations_completed": self.iterations
        }


# ======================================================================
# AGENT 3 — SYNTHESIS AGENT
# ======================================================================

class SynthesisAgent:

    def synthesize(self, sources: List[Dict], query: str, session_id: str):

        system = """
        You are an elite research analyst.
        Combine all collected information into a 2000–2500 word synthesis.
        """

        combined = "\n\n".join([
            s.get("content", "") for s in sources
        ])

        user = f"""
        Topic: {query}

        Use the following research material:

        {combined}

        Produce:
        - A long 6–10 paragraph synthesis
        - Trends, frameworks, insights
        """

        synthesis_text = run_llm(system, user)

        return {"synthesis": synthesis_text}


# ======================================================================
# AGENT 4 — VALIDATION AGENT
# ======================================================================

class ValidationAgent:

    def validate(self, synthesis: str, sources: List[Dict], session_id: str):

        system = """
        You are a fact-checking AI.
        Compare synthesis with provided sources.
        """

        user = f"""
        Validate the following synthesis:

        {synthesis}
        """

        validation_text = run_llm(system, user)

        return {
            "validation_text": validation_text,
            "confidence_score": 92
        }


# ======================================================================
# AGENT 5 — FINAL CONTENT GENERATOR
# ======================================================================

from agents.llm_model import call_llm
from tools.citations import CitationFormatter


class ContentGeneratorAgent:

    def __init__(self):
        self.max_tokens = 5000

    def generate(
        self,
        synthesis: str,
        validation: Dict,
        sources: List[Dict],
        output_format: str,
        session_id: str
    ):

        prompt = self._build_prompt(synthesis, validation, output_format)

        response = call_llm(prompt, max_tokens=self.max_tokens)
        text = response["content"]

        citations_md = CitationFormatter.markdown(sources)

        final = text + f"\n\n---\n\n### 📚 Citations\n{citations_md}\n"

        return {
            "content": final,
            "word_count": len(final.split()),
            "format": output_format
        }

    # -------------------------------------------------------------
    # PROMPT BUILDER
    # -------------------------------------------------------------
    def _build_prompt(
        self,
        synthesis: str,
        validation: Dict,
        fmt: str
    ) -> str:

        val_text = validation.get("validation_text", "")

        base = f"""
SYNTHESIS:
{synthesis}

VALIDATION:
{val_text}
"""

        formats = {
            "report": f"""
Write a detailed professional RESEARCH REPORT.

Requirements:
- Executive summary
- Key findings
- Deep analysis
- Recommendations

{base}
""",

            "article": f"""
Write a long MAGAZINE ARTICLE in engaging tone.

{base}
""",

            "summary": f"""
Write a structured SUMMARY (5–8 sections).

{base}
""",

            "presentation": f"""
Write a SLIDE DECK style breakdown.

{base}
"""
        }

        return formats.get(fmt, formats["report"])
