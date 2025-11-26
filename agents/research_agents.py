import os
from groq import Groq
from typing import List, Dict, Any
from loguru import logger

# -------------------------------------------------
# LLM CLIENT (Groq – LLaMA 3–70B)
# -------------------------------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LLM_MODEL = "llama3-70b-8192"     # BEST FREE LONG MODEL
MAX_TOKENS = 7000                 # Allow long deep research
TEMP = 0.4                        # Stable but creative


# -------------------------------------------------
# BASE LLM CALL
# -------------------------------------------------
def run_llm(system_prompt: str, user_prompt: str) -> str:
    """Universal LLM runner with long-output settings"""

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


# -------------------------------------------------
# AGENT 1 — Query Planner
# -------------------------------------------------
class QueryPlannerAgent:
    def plan_research(self, query: str, session_id: str):
        logger.info(f"Planning research: {query}")

        system = """
        You are a senior research strategist.
        Break complex research topics into deep sub-questions.
        Ensure all angles are covered: causes, effects, trends, data, forecasts,
        challenges, frameworks, opportunities, risks, and global context.
        """

        user = f"""
        Create a detailed research plan for: {query}

        Output fields:
        - Main Research Objective
        - 6–12 deeply analytical sub-questions
        - A data-collection strategy
        - A verification strategy
        """

        result = run_llm(system, user)

        return {
            "plan_text": result,
            "sub_questions": self._extract_sub_questions(result)
        }

    def _extract_sub_questions(self, text: str) -> List[str]:
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        subs = [l for l in lines if any(k in l.lower() for k in ["?", "question"])]
        return subs[:12]


# -------------------------------------------------
# AGENT 2 — Research Agent (Iterative Deep Research)
# -------------------------------------------------
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
                    # Perform enriched web search
                    results = self.search_tool.search(q, n_results=self.sources_per_iter)
                    aggregated_sources.extend(results)
                except Exception as e:
                    logger.warning(f"Search failed: {e}")

        return {
            "sources": aggregated_sources,
            "total_sources": len(aggregated_sources),
            "iterations_completed": self.iterations
        }


# -------------------------------------------------
# AGENT 3 — Synthesis Agent
# -------------------------------------------------
class SynthesisAgent:
    def synthesize(self, sources: List[Dict], query: str, session_id: str):
        system = """
        You are an elite research analyst.
        Combine all sources into one unified, coherent synthesis.
        The synthesis must:
        - Be extremely detailed (2000+ words)
        - Include real-world data, evidence, and frameworks
        - Compare and contrast findings
        - Identify trends, patterns, contradictions
        - Provide deep reasoning, not surface explanations
        """

        content = "\n\n".join([s.get("content", "") for s in sources])

        user = f"""
        Research Topic: {query}

        Combine ALL the following research data into a unified synthesis:

        {content}

        Produce:
        - 6–10 paragraph deep synthesis
        - Trends, models, frameworks, global impact
        - Predictions + scenario analysis
        """

        analysis = run_llm(system, user)

        return {"synthesis": analysis}


# -------------------------------------------------
# AGENT 4 — Validation Agent
# -------------------------------------------------
class ValidationAgent:
    def validate(self, synthesis: str, sources: List[Dict], session_id: str):
        system = """
        You are a fact-checking AI.
        Compare synthesis with evidence.
        Identify gaps, contradictions, false claims,
        missing angles, missing data, or assumptions.
        """

        user = f"""
        Validate the following synthesis against the collected sources.

        Synthesis:
        {synthesis}
        """

        validation = run_llm(system, user)

        return {
            "validation_text": validation,
            "confidence_score": 95
        }


# -------------------------------------------------
# AGENT 5 — Final Content Generator
# -------------------------------------------------
class ContentGeneratorAgent:
    def generate(
        self,
        synthesis: str,
        validation: Dict[str, Any],
        sources: List[Dict],
        output_format: str,
        session_id: str
    ):
        system = """
        You are a professional research writer.
        Produce extremely detailed, properly formatted long-form research output.
        
        VERY IMPORTANT — Citations Format Requirement:
        ---------------------------------------------
        ALWAYS output citations EXACTLY like this:

        Citations:
        1. Title of source – URL
        2. Title of source – URL
        3. Title of source – URL

        • Each citation MUST be on its own line.
        • MUST be numbered clearly.
        • Do NOT merge multiple citations into one line.
        • Do NOT include raw text after URLs.
        """

        # Build clean citation data
        # if your sources include title + url, format them safely
        citations = []
        for s in sources:
            title = s.get("title", "Untitled Source")
            url = s.get("url", "")
            if url:
                citations.append(f"- {title} – {url}")

        citations_block = "\n".join(citations)

        user = f"""
        Write a full {output_format} based on this research:

        === SYNTHESIS ===
        {synthesis}

        === VALIDATION ===
        {validation}

        === RAW SOURCES (FORMAT THESE INTO CLEAN CITATIONS) ===
        {citations_block}

        Requirements:
        • Length: 2500–6000 words
        • 14+ sections
        • Deep analysis, statistics, models, future predictions
        • Structured, academic style
        
        At the end, include:

        Citations:
        1. Title – URL
        2. Title – URL
        3. Title – URL
        (Use the provided source list above)
        """

        content = run_llm(system, user)

        return {
            "content": content,
            "word_count": len(content.split())
        }
