"""
FAST Groq-Only Research Agents (fixed & crash-proof)
Model: llama-3.1-8b-instant (via Groq)
Uses: GROQ_API_KEY from environment / .env
This file is a robust, minimal drop-in replacement for agents.research_agents.
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from loguru import logger
from observability.logger import observability
from tools.web_search_tool import WebSearchTool, CitationFormatter
from memory.memory_bank import MemoryBank, ContextCompactor


# -----------------------------
# Groq Client (robust)
# -----------------------------
class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        # use a stable, small model by default for local testing
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        self.url = "https://api.groq.com/openai/v1/chat/completions"

        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY missing! Set GROQ_API_KEY in your .env")

        # quick debug print to confirm initialization
        print(f"Groq Client Loaded → Model: {self.model}")

    def chat(self, system_prompt: str, user_prompt: str, max_tokens: int = 2048, timeout: int = 30) -> str:
        """
        Send a chat request to Groq (OpenAI-compatible endpoint).
        Returns text content or raises RuntimeError with details.
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.2
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            resp = requests.post(self.url, json=payload, headers=headers, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            # safe navigation: handle multiple shapes of response
            try:
                return data["choices"][0]["message"]["content"]
            except Exception:
                # fallback: some APIs return a simple "text"
                if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                    choice = data["choices"][0]
                    if isinstance(choice, dict):
                        # try multiple common keys
                        for k in ("message", "text", "content"):
                            if k in choice:
                                if isinstance(choice[k], dict) and "content" in choice[k]:
                                    return choice[k]["content"]
                                return choice[k]
                raise RuntimeError("Unexpected response shape from Groq: " + json.dumps(data)[:1000])

        except requests.exceptions.HTTPError as he:
            logger.error(f"Groq HTTP error: {he} - Response: {getattr(he.response, 'text', '')}")
            raise RuntimeError(f"Groq HTTP error: {he} - {getattr(he.response, 'text', '')}")
        except requests.exceptions.RequestException as re:
            logger.error(f"Groq Request exception: {re}")
            raise RuntimeError(f"Groq Request exception: {re}")
        except ValueError as ve:
            logger.error(f"Groq JSON decode error: {ve}")
            raise RuntimeError(f"Groq JSON decode error: {ve}")


# ============================================================
# Base Agent
# ============================================================
class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        print(f"\n=== Initializing Agent: {name} ===")
        self.llm = GroqClient()

    def _call_llm(self, system_prompt: str, user_message: str, max_tokens: int = 2048) -> str:
        """
        Centralized LLM call with observability logging.
        Returns string or raises RuntimeError.
        """
        try:
            return self.llm.chat(system_prompt, user_message, max_tokens=max_tokens)
        except Exception as e:
            logger.error(f"{self.name} LLM call failed: {e}")
            raise


# ============================================================
# Query Planner Agent
# ============================================================
class QueryPlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("QueryPlanner")
        self.system_prompt = """
You quickly convert any topic into a compact, valid JSON research plan.
Keep output minimal and valid JSON. Use the exact JSON shape shown.

Format:
{
 "main_topic": "...",
 "sub_questions": [
   {"question":"...", "priority":1, "keywords":["..."]}
 ],
 "estimated_sources_needed": 6
}
"""

    def plan_research(self, query: str, session_id: str) -> Dict[str, Any]:
        logger.info(f"Planning research: {query}")
        user_message = f"Generate a minimal JSON research plan for: {query}"

        try:
            reply = self._call_llm(self.system_prompt, user_message, max_tokens=700)
            # safe parse: strip bytes and attempt to find JSON block
            plan = self._safe_load_json(reply)
            if not isinstance(plan, dict):
                raise ValueError("Plan is not a dict")
            # normalize: ensure expected keys exist
            if "sub_questions" not in plan or not isinstance(plan["sub_questions"], list):
                plan["sub_questions"] = [{"question": query, "priority": 5, "keywords": query.split()}]
            if "main_topic" not in plan:
                plan["main_topic"] = query
            if "estimated_sources_needed" not in plan:
                plan["estimated_sources_needed"] = 6
            return plan

        except Exception as e:
            logger.warning(f"QueryPlanner fallback due to: {e}")
            # deterministic fallback
            return {
                "main_topic": query,
                "sub_questions": [
                    {"question": query, "priority": 5, "keywords": query.split()}
                ],
                "estimated_sources_needed": 6
            }

    @staticmethod
    def _safe_load_json(text: str) -> Any:
        """
        Attempt to extract JSON from LLM reply safely.
        If the full reply is JSON, parse directly; otherwise attempt to find the first JSON object.
        """
        if not text:
            return {}
        text = text.strip()
        # quick attempt
        try:
            return json.loads(text)
        except Exception:
            # attempt to find first '{' ... '}' block
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(text[start:end + 1])
                except Exception:
                    pass
        # last resort: empty dict
        return {}


# ============================================================
# Research Agent (Web Search)
# ============================================================
class ResearchAgent(BaseAgent):
    def __init__(self, search_tool: WebSearchTool):
        super().__init__("Researcher")
        self.search_tool = search_tool
        self.max_iterations = 3  # fast mode
        self.system_prompt = """
Identify missing info and propose next search queries.
Return compact JSON:
{
 "next_search":["..."],
 "need_more": true/false
}
"""

    def research(self, sub_questions: List[Dict[str, Any]], session_id: str, memory_bank: MemoryBank) -> Dict[str, Any]:
        all_sources: List[Dict[str, Any]] = []
        research_log: List[Dict[str, Any]] = []

        for iteration in range(self.max_iterations):
            if iteration == 0:
                queries = [s.get("question") or "" for s in sub_questions]
            else:
                gap = self._identify_gaps(all_sources, sub_questions)
                if not gap or not gap.get("need_more", False):
                    break
                queries = gap.get("next_search", []) or []

            iteration_sources: List[Dict[str, Any]] = []

            for q in queries[:2]:  # limit to 2 queries per iteration in FAST mode
                if not q:
                    continue
                try:
                    result = self.search_tool.search(q, max_results=4)
                except Exception as e:
                    logger.warning(f"Search tool failed for query '{q}': {e}")
                    result = {"results": []}

                for source in result.get("results", []):
                    # normalize source fields and guard against None
                    normalized = {
                        "url": source.get("url", "") or "",
                        "title": source.get("title", "") or "",
                        # ensure content is string not None
                        "content": (source.get("content") or "") if source.get("content") is not None else "",
                        "relevance_score": source.get("relevance_score", 0.5),
                        "metadata": source.get("metadata", {}) or {}
                    }
                    iteration_sources.append(normalized)
                    # store in memory
                    try:
                        memory_bank.store_source(
                            url=normalized["url"],
                            title=normalized["title"],
                            content=normalized["content"],
                            relevance=normalized.get("relevance_score", 0.5),
                            metadata={"iteration": iteration, "query": q, **(normalized.get("metadata") or {})}
                        )
                    except Exception as me:
                        logger.warning(f"Failed to store in memory bank: {me}")

            all_sources.extend(iteration_sources)
            research_log.append({
                "iteration": iteration + 1,
                "queries": queries,
                "sources_found": len(iteration_sources)
            })

        # ensure total_sources and iterations_completed exist (orchestrator expects them)
        total_sources = len(all_sources)
        return {
            "sources": all_sources,
            "research_log": research_log,
            "iterations_completed": len(research_log),
            "total_sources": total_sources
        }

    def _identify_gaps(self, sources: List[Dict[str, Any]], sub_questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        # build a compact summary of top sources (safe get)
        sources_text = "\n".join([(s.get("content") or "")[:220] for s in (sources or [])[:4]])
        questions_text = "\n".join([f"- {sq.get('question') or ''}" for sq in (sub_questions or [])[:6]])

        user_message = f"Sub-questions:\n{questions_text}\n\nSources summary:\n{sources_text}\n\nReturn JSON with next_search (list) and need_more boolean."
        try:
            reply = self._call_llm(self.system_prompt, user_message, max_tokens=300)
            parsed = QueryPlannerAgent._safe_load_json(reply)
            # normalize keys
            if not isinstance(parsed, dict):
                return {"next_search": [], "need_more": False}
            next_search = parsed.get("next_search") or parsed.get("next_search_queries") or parsed.get("next_searches") or []
            need_more = bool(parsed.get("need_more", parsed.get("need_more_research", False)))
            # ensure list
            if not isinstance(next_search, list):
                next_search = [str(next_search)] if next_search else []
            return {"next_search": next_search, "need_more": need_more}
        except Exception as e:
            logger.warning(f"_identify_gaps LLM error: {e}")
            return {"next_search": [], "need_more": False}


# ============================================================
# Synthesis Agent
# ============================================================
class SynthesisAgent(BaseAgent):
    def __init__(self):
        super().__init__("Synthesizer")
        self.system_prompt = "Write a short, fast synthesis from the given sources. Focus on main findings and confidence."

    def synthesize(self, sources: List[Dict[str, Any]], query: str, session_id: str) -> Dict[str, Any]:
        compacted = ContextCompactor(max_tokens=1500).compact_sources(sources or [], target_tokens=1200)
        # safe build of content text
        text = "\n\n".join([(s.get("title") or "") + "\n" + (s.get("content") or "")[:400] for s in compacted[:8]])
        user_message = f"Query: {query}\n\nSources:\n{text}\n\nWrite a concise synthesis (2-4 paragraphs)."

        try:
            out = self._call_llm(self.system_prompt, user_message, max_tokens=900)
            synthesis_text = out or ""
            return {"synthesis": synthesis_text, "sources_used": len(compacted), "synthesis_length": len(synthesis_text.split())}
        except Exception as e:
            logger.warning(f"Synthesis failed: {e}")
            return {"synthesis": "", "sources_used": len(compacted), "synthesis_length": 0}


# ============================================================
# Validation Agent
# ============================================================
class ValidationAgent(BaseAgent):
    def __init__(self):
        super().__init__("Validator")
        self.system_prompt = "Validate the synthesis against the listed sources. Return minimal JSON."

    def validate(self, synthesis: str, sources: List[Dict[str, Any]], session_id: str) -> Dict[str, Any]:
        refs = "\n".join([(s.get("title") or "") + " - " + (s.get("url") or "") for s in (sources or [])[:6]])
        # produce a safe JSON-return instruction (avoid single braces inside f-string)
        user_message = "SYNTHESIS:\\n{}\\n\\nSOURCES:\\n{}\\n\\nReturn JSON with keys: status, confidence (0-100), gaps (list)".format(synthesis, refs)

        try:
            reply = self._call_llm(self.system_prompt, user_message, max_tokens=400)
            parsed = QueryPlannerAgent._safe_load_json(reply)
            if not isinstance(parsed, dict):
                raise ValueError("Invalid validation response")
            # normalize keys
            status = parsed.get("status") or parsed.get("validation_status") or "needs_review"
            confidence = parsed.get("confidence") or parsed.get("confidence_score") or 70
            gaps = parsed.get("gaps") or []
            if not isinstance(gaps, list):
                gaps = [str(gaps)]
            return {"status": status, "confidence": int(confidence or 0), "gaps": gaps}
        except Exception as e:
            logger.warning(f"Validation fallback: {e}")
            return {"status": "needs_review", "confidence": 70, "gaps": []}


# ============================================================
# Content Generator Agent
# ============================================================
class ContentGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("ContentGenerator")
        self.system_prompt = "Write clear, concise content from synthesis and validation notes."

    def generate(self, synthesis: str, validation: Dict[str, Any], sources: List[Dict[str, Any]], format_type: str = "report", session_id: Optional[str] = None) -> Dict[str, Any]:
        citations = CitationFormatter.format_citations((sources or [])[:6])
        cites_text = "\n".join(citations)
        user_message = f"Format: {format_type}\\n\\nSYNTHESIS:\\n{synthesis}\\n\\nVALIDATION:\\n{validation}\\n\\nCITATIONS:\\n{cites_text}\\n\\nWrite the final deliverable."

        try:
            out = self._call_llm(self.system_prompt, user_message, max_tokens=1200)
            content_text = out or ""
            return {"content": content_text, "word_count": len(content_text.split()), "citations": citations, "format": format_type}
        except Exception as e:
            logger.warning(f"Content generation failed: {e}")
            return {"content": "", "word_count": 0, "citations": citations, "format": format_type}
