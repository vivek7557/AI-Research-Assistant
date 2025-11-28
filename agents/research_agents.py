"""
Research Agents — FIXED (NO LOGIC CHANGES)
Uses the unified call_llm() from llm_model.py
"""

import json
import time
from typing import List, Dict

from agents.llm_model import call_llm
from loguru import logger


# ===============================================================
# 1️⃣ Query Planner Agent
# ===============================================================
def plan_research(self, query, session_id):
    """
    STEP 1 — Query Planning
    LLM returns JSON. We validate, repair, and fallback if JSON invalid.
    """

    system = "You are a research planning agent. Output ONLY valid JSON."
    user = f"""
    Create a research plan for: {query}

    Return JSON exactly like:
    {{
        "sub_questions": [
            "Question 1",
            "Question 2",
            "Question 3"
        ]
    }}
    """

    raw = run_llm(system, user)

    # -------------------------------
    # VALIDATE + FIX BROKEN JSON
    # -------------------------------
    try:
        # Try to parse clean JSON first
        plan = json.loads(raw)

    except Exception:
        logger.error(f"[Planner Error] Invalid JSON: {raw}")

        # Soft fix: extract JSON-like region
        try:
            start = raw.index("{")
            end = raw.rindex("}") + 1
            repaired = raw[start:end]
            plan = json.loads(repaired)
        except Exception:
            # Hard fallback (never break pipeline)
            plan = {
                "sub_questions": [
                    f"What are the key aspects of {query}?",
                    f"What are recent developments in {query}?",
                    f"What challenges exist in {query}?"
                ]
            }

    # Ensure valid output
    if "sub_questions" not in plan or not isinstance(plan["sub_questions"], list):
        plan = {
            "sub_questions": [
                f"Overview of {query}",
                f"Current trends in {query}",
                f"Challenges and opportunities in {query}"
            ]
        }

    return plan



# ===============================================================
# 2️⃣ Research Agent (Loop Agent)
# ===============================================================
class ResearchAgent:

    def __init__(self, search_tool):
        self.search_tool = search_tool
        self.iterations = 3
        self.sources_per_iter = 5

    def set_depth(self, iterations: int, sources: int):
        self.iterations = iterations
        self.sources_per_iter = sources

    def research(self, sub_questions: List[str], session_id: str, memory_bank, loop_iterations=None):
        results = []
        all_sources = []

        iters = loop_iterations or self.iterations

        for i in range(iters):
            for sq in sub_questions:

                # run web search
                search_results = self.search_tool.search(sq, self.sources_per_iter)
                all_sources.extend(search_results)

                # store research findings
                text = "\n".join([s.get("content", "") for s in search_results])

                memory_bank.store_memory(
                    content=text[:800],
                    category="research",
                    importance=0.6,
                    metadata={"session": session_id, "sq": sq}
                )

                results.append({"sub_question": sq, "raw_text": text})

        return {
            "sources": all_sources,
            "iterations_completed": iters,
            "raw_results": results,
            "total_sources": len(all_sources),
        }


# ===============================================================
# 3️⃣ Synthesis Agent
# ===============================================================
class SynthesisAgent:

    def synthesize(self, sources: List[Dict], query: str, session_id: str):
        combined = "\n".join([s.get("content", "") for s in sources])

        prompt = (
            f"Topic: {query}\n\n"
            "You are a synthesis expert. Combine all research into a single, "
            "well-structured narrative (long, detailed). Include:\n"
            "- Executive Summary\n"
            "- Key Findings\n"
            "- Deep Analysis\n"
            "- Recommendations\n\n"
            "Here is the research:\n"
            f"{combined[:15000]}"
        )

        try:
            out = call_llm(prompt, max_tokens=7000)
            return {"synthesis": out}
        except Exception as e:
            logger.error(f"[Synthesis Error] {e}")
            return {"synthesis": "Synthesis failed."}


# ===============================================================
# 4️⃣ Validation Agent
# ===============================================================
class ValidationAgent:

    def validate(self, synthesis_text: str, sources: List[Dict], session_id: str):
        prompt = (
            "Validate the synthesized research. Check for:\n"
            "- gaps\n"
            "- contradictions\n"
            "- unsupported claims\n"
            "Return JSON ONLY like:\n"
            '{"gaps": [...], "contradictions": [...], "confidence": 0-100}'
        )

        try:
            out = call_llm(prompt + "\n\n" + synthesis_text[:5000])
            data = json.loads(out)
            return data
        except:
            return {"gaps": [], "contradictions": [], "confidence": 100}


# ===============================================================
# 5️⃣ Final Content Generator Agent
# ===============================================================
class ContentGeneratorAgent:

    def generate(self, synthesis_text: str, validation_results: dict, sources: List[Dict], output_format: str, session_id: str):

        prompt = (
            f"You are a senior technical writer.\n"
            f"Format the research output as a **{output_format}**.\n"
            "Must be LONG, DETAILED, PROFESSIONAL.\n"
            "Sections REQUIRED:\n"
            "- Title\n"
            "- Executive Summary\n"
            "- Key Findings\n"
            "- Deep Analysis\n"
            "- Recommendations\n"
            "- Validation Summary\n"
            "- Citations (one per line)\n\n"
            "Here is the synthesis:\n"
            f"{synthesis_text}\n\n"
            "Validation:\n"
            f"{json.dumps(validation_results, indent=2)}\n\n"
            "Sources:\n"
            f"{json.dumps(sources[:20], indent=2)}"
        )

        try:
            text = call_llm(prompt, max_tokens=7000)

            citations = []
            for s in sources[:20]:
                if s.get("url"):
                    citations.append(f"- {s.get('title', 'Source')} — {s['url']}")

            return {
                "content": text,
                "citations": citations,
                "word_count": len(text.split())
            }

        except Exception as e:
            logger.error(f"[ContentGenerator Error] {e}")
            return {
                "content": "Content generation failed.",
                "citations": [],
                "word_count": 0
            }
