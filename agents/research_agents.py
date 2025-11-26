"""
Research Agents — Query Planner, Research Agent (Loop), Synthesizer,
Validator and Content Generator.

UPDATED: Supports dynamic depth configuration from ResearchOrchestrator
"""

import json
import traceback
from typing import List, Dict, Any, Optional

from loguru import logger
from tools.web_search_tool import WebSearchTool
from base.agent_base import BaseAgent
from memory.memory_bank import MemoryBank


# ============================================================
# 1. QUERY PLANNER AGENT
# ============================================================
class QueryPlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("QueryPlanner")
        self.system_prompt = """
Break down the research query into sub-questions.

Return JSON ONLY:
{
 "sub_questions": ["...", "..."]
}
"""

    def plan_research(self, query: str, session_id: str):
        logger.info(f"Planning research: {query}")

        response = self.run_llm(
            system=self.system_prompt,
            user=f"Break this research question into actionable sub-questions:\n\n{query}"
        )

        try:
            data = json.loads(response)
        except Exception:
            data = {"sub_questions": [query]}

        return data


# ============================================================
# 2. RESEARCH AGENT (LOOP) — UPDATED FOR DEPTH SUPPORT
# ============================================================
class ResearchAgent(BaseAgent):
    def __init__(self, search_tool: WebSearchTool):
        super().__init__("Researcher")
        self.search_tool = search_tool
        self.max_iterations = 3  # default if depth not passed

        self.gap_prompt = """
Analyze the research collected so far and decide:
- What information is missing?
- What next search queries should be run?

Return JSON ONLY:
{
 "next_search": ["query1", "query2"],
 "need_more": true/false
}
"""

    # ---------------------------
    # MAIN LOOP
    # ---------------------------
    def research(
        self,
        sub_questions: List[str],
        session_id: str,
        memory_bank: MemoryBank,
        loop_iterations: Optional[int] = None
    ) -> Dict[str, Any]:

        # Dynamically override iteration count if depth is set
        if loop_iterations is not None:
            self.max_iterations = loop_iterations

        logger.info(f"Research Loop: Running {self.max_iterations} iterations")

        all_sources = []
        research_log = []

        for iteration in range(self.max_iterations):

            # ---- Iteration 0 → Use sub-questions
            if iteration == 0:
                queries = sub_questions[:3]  # use first 3 only

            # ---- Later iterations → Use gap analysis
            else:
                gap = self._identify_gaps(all_sources, sub_questions)

                if not gap or not gap.get("need_more", False):
                    logger.info("No more gaps detected — stopping early.")
                    break

                queries = gap.get("next_search", [])[:3]

            iteration_sources = []

            # ------------------------
            # EXECUTE SEARCH QUERIES
            # ------------------------
            for q in queries:
                if not q or len(q.strip()) == 0:
                    continue

                logger.info(f"[Iteration {iteration+1}] Searching: {q}")

                try:
                    result = self.search_tool.search(q, max_results=5)
                except Exception as e:
                    logger.warning(f"Search failed for '{q}': {e}")
                    continue

                for src in result.get("results", []):
                    processed = {
                        "url": src.get("url", ""),
                        "title": src.get("title", "No title"),
                        "content": src.get("content", ""),
                        "relevance_score": src.get("relevance_score", 0.5),
                        "metadata": src.get("metadata", {})
                    }

                    iteration_sources.append(processed)

                    # Save in memory
                    try:
                        memory_bank.store_source(
                            url=processed["url"],
                            title=processed["title"],
                            content=processed["content"],
                            relevance=processed["relevance_score"],
                            metadata={"iteration": iteration, "query": q}
                        )
                    except Exception as mem_err:
                        logger.warning(f"Memory save error: {mem_err}")

            # End iteration
            all_sources.extend(iteration_sources)
            research_log.append({
                "iteration": iteration + 1,
                "queries": queries,
                "sources_found": len(iteration_sources)
            })

        return {
            "sources": all_sources,
            "research_log": research_log,
            "iterations_completed": len(research_log),
            "total_sources": len(all_sources)
        }

    # ---------------------------
    # GAP IDENTIFICATION
    # ---------------------------
    def _identify_gaps(self, sources: List[Dict], sub_questions: List[str]) -> Dict[str, Any]:
        try:
            response = self.run_llm(
                system=self.gap_prompt,
                user=f"""
Here are the sources found so far:

{savestr(sources)}

Sub-questions:
{sub_questions}
"""
            )

            return json.loads(response)

        except Exception as e:
            logger.warning(f"Gap analysis failed: {e}")
            return {"next_search": sub_questions, "need_more": False}


# ============================================================
# 3. SYNTHESIS AGENT
# ============================================================
class SynthesisAgent(BaseAgent):
    def __init__(self):
        super().__init__("Synthesizer")
        self.system_prompt = """
Synthesize multiple research sources into a coherent narrative.
Return detailed text.
"""

    def synthesize(self, sources: List[Dict], query: str, session_id: str):
        text = "\n\n".join([s.get("content", "") for s in sources[:10]])

        response = self.run_llm(
            system=self.system_prompt,
            user=f"Synthesize these findings regarding:\n\n{query}\n\n{text}"
        )

        return {"synthesis": response}


# ============================================================
# 4. VALIDATION AGENT
# ============================================================
class ValidationAgent(BaseAgent):
    def __init__(self):
        super().__init__("Validator")
        self.system_prompt = """
Validate accuracy, detect contradictions, find missing evidence.
Return JSON ONLY:
{
 "gaps": [...],
 "contradictions": [...],
 "confidence_score": 0-100
}
"""

    def validate(self, synthesis: str, sources: List[Dict], session_id: str):
        try:
            response = self.run_llm(
                system=self.system_prompt,
                user=f"Validate this synthesis:\n{synthesis}"
            )
            return json.loads(response)
        except Exception:
            logger.warning("Validation LLM error — using fallback.")
            return {
                "gaps": [],
                "contradictions": [],
                "confidence_score": 70
            }


# ============================================================
# 5. CONTENT GENERATOR AGENT
# ============================================================
class ContentGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("ContentGenerator")

        # Ultra-Deep Research Prompts (MAX LENGTH + MAX QUALITY)
        self.prompts = {
            "report": """
You are an elite research writer. Produce a **full academic research report** with
minimum **3000–4000 words** and deep analytical depth.

Your report MUST include ALL sections below, each very detailed:

=========================================================
1. TITLE PAGE  
2. EXECUTIVE SUMMARY (200–300 words)  
3. INTRODUCTION (600–800 words)  
4. PROBLEM BACKGROUND  
   - Historical evolution  
   - Scientific explanation  
   - Current global trends with year-wise progression  
5. DATA & STATISTICAL ANALYSIS  
   - Include comparative tables  
   - Include trend graph (ASCII format)  
   - Include metrics from multiple frameworks  
6. DETAILED RESEARCH FINDINGS  
   - 8–12 insights  
   - Each insight must be 150+ words  
7. IMPACT ANALYSIS  
   - Environmental  
   - Economic  
   - Geopolitical  
   - Social + cultural  
8. CASE STUDIES (3–5 case studies, each 200–300 words)  
9. TECHNOLOGY & AI INFLUENCE  
10. POLICY ANALYSIS  
11. FUTURE SCENARIOS (2030, 2040, 2050)  
12. RISKS, CHALLENGES & LIMITATIONS  
13. RECOMMENDATIONS (10 actionable points)  
14. CONCLUSION (250–350 words)  
15. REFERENCES (APA-style)  
=========================================================

STRICT RULES:
- Minimum length: **3000+ words**.  
- NO sentence repetition.  
- NO vague content.  
- Each section must be high-depth.  
- Use bullet points, tables, diagrams.  
- Academic, polished, expert-level writing.
""",

            "article": """
Write a 2000+ word expert long-form editorial with deep reasoning,
case studies, storytelling, and multiple analytical layers.
""",

            "summary": """
Write a 700–1000 word executive summary.
""",

            "presentation": """
Write a 25–slide outline with talking points and speaker notes.
"""
        }

    def generate(self, synthesis, validation, sources, fmt, session_id):

        prompt = self.prompts.get(fmt, self.prompts["report"])

        result = self.run_llm(
            system=prompt,
            user=f"""
Write a full-length research output using the following:

SYNTHESIS:
{synthesis}

VALIDATION:
{json.dumps(validation, indent=2)}

TOP SOURCES:
{json.dumps([s.get('url','') for s in sources], indent=2)}

Your output MUST follow the exact structure and depth requirement.
"""
        )

        return {
            "format": fmt,
            "content": result,
            "word_count": len(result.split())
        }
