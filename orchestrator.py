"""
Research Orchestrator
Coordinates all agents in a sequential and loop-based workflow
Implements multi-agent system architecture
"""

import uuid
import time
import json
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from loguru import logger

from agents.research_agents import (
    QueryPlannerAgent,
    ResearchAgent,
    SynthesisAgent,
    ValidationAgent,
    ContentGeneratorAgent
)

from tools.web_search_tool import WebSearchTool
from memory.memory_bank import SessionManager, MemoryBank, ContextCompactor
from observability.logger import observability



class ResearchOrchestrator:
    """
    MAIN PIPELINE:
        1. Query Planning  
        2. Research (LOOP with depth control)  
        3. Synthesis  
        4. Validation  
        5. Final Content Generation  
    """

    def __init__(self):
        # Tools
        self.search_tool = WebSearchTool()

        # Agents
        self.query_planner = QueryPlannerAgent()
        self.researcher = ResearchAgent(self.search_tool)
        self.synthesizer = SynthesisAgent()
        self.validator = ValidationAgent()
        self.content_generator = ContentGeneratorAgent()

        # Memory
        self.session_manager = SessionManager()
        self.memory_bank = MemoryBank()
        self.context_compactor = ContextCompactor()

        logger.info("Research Orchestrator initialized.")

    # ================================================================
    # MAIN RESEARCH PIPELINE
    # ================================================================
    def conduct_research(
        self,
        query: str,
        output_format: str = "report",
        session_id: Optional[str] = None,
        depth: int = 3
    ) -> Dict[str, Any]:

        observability.start_session()

        try:
            # -----------------------------------------------------
            # PREP: SESSION
            # -----------------------------------------------------
            if not session_id:
                session_id = f"research_{uuid.uuid4().hex[:8]}"

            self.session_manager.create_session(session_id, query)
            logger.info(f"Starting research session: {session_id}")

            # -----------------------------------------------------
            # DEPTH LOGIC (UPDATED + FIXED)
            # -----------------------------------------------------
            # Depth affects iterations (loop cycles) and number of sources per iteration
            depth_config = {
                1: (1, 2),   # ultra fast
                2: (2, 3),   # fast
                3: (3, 5),   # normal
                4: (4, 7),   # deep
                5: (6, 10),  # ultra deep
            }

            iterations, sources_per_iter = depth_config.get(depth, (3, 5))

            logger.info(
                f"[DEPTH CONFIG] depth={depth} → "
                f"iterations={iterations}, sources_per_iter={sources_per_iter}"
            )

            if hasattr(self.researcher, "set_depth"):
                self.researcher.set_depth(iterations, sources_per_iter)

            # -----------------------------------------------------
            # STAGE 1 — Query Planning
            # -----------------------------------------------------
            plan = self._stage_planning(query, session_id)

            # -----------------------------------------------------
            # STAGE 2 — Research LOOP
            # -----------------------------------------------------
            research_results = self._stage_research(
                plan, session_id, iterations
            )

            # -----------------------------------------------------
            # STAGE 3 — Synthesis
            # -----------------------------------------------------
            synthesis_results = self._stage_synthesis(
                research_results,
                query,
                session_id
            )

            # -----------------------------------------------------
            # STAGE 4 — Validation
            # -----------------------------------------------------
            validation_results = self._stage_validation(
                synthesis_results,
                research_results["sources"],
                session_id
            )

            # -----------------------------------------------------
            # STAGE 5 — Final Content Generation
            # -----------------------------------------------------
            final_content = self._stage_generation(
                synthesis_results,
                validation_results,
                research_results["sources"],
                output_format,
                session_id
            )

            # -----------------------------------------------------
            # SESSION FINALIZATION
            # -----------------------------------------------------
            session_data = self.session_manager.get_session(session_id)
            session_data["duration"] = time.time() - time.mktime(
                time.strptime(session_data["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            )

            self.memory_bank.store_research_session(session_data)
            self.session_manager.close_session(session_id, "completed")
            observability.end_session("completed")

            # -----------------------------------------------------
            # FINAL RESULT OBJECT
            # -----------------------------------------------------
            return {
                "session_id": session_id,
                "query": query,
                "plan": plan,
                "research_summary": {
                    "total_sources": research_results["total_sources"],
                    "iterations": research_results["iterations_completed"]
                },
                "synthesis": synthesis_results["synthesis"],
                "validation": validation_results,
                "final_content": final_content,
                "metrics": observability.get_metrics_summary(),
                "memory_stats": self.memory_bank.get_statistics(),
                "depth_used": depth
            }

        except Exception as e:
            logger.error(f"Research failed: {str(e)}")
            observability.end_session("failed")
            raise

    # ================================================================
    # STAGE HANDLERS
    # ================================================================
    def _stage_planning(self, query: str, session_id: str) -> Dict[str, Any]:
        """Stage 1: Planning"""
        plan = self.query_planner.plan_research(query, session_id)

        self.session_manager.update_session(session_id, {
            "current_stage": "research",
            "sub_queries": plan.get("sub_questions", [])
        })

        self.memory_bank.store_memory(
            f"Plan created for: {query}",
            "planning",
            0.8,
            {"plan": plan}
        )

        self.session_manager.set_agent_output(session_id, "QueryPlanner", plan)
        return plan

    def _stage_research(
        self,
        plan: Dict[str, Any],
        session_id: str,
        iterations: int
    ) -> Dict[str, Any]:

        sub_questions = plan.get("sub_questions", [])
        logger.info(f"Executing research loop: {iterations} iterations")

        results = self.researcher.research(
            sub_questions,
            session_id,
            self.memory_bank,
            loop_iterations=iterations   # <--- ensures depth works
        )

        self.session_manager.update_session(session_id, {
            "current_stage": "synthesis",
            "sources_found": results["sources"],
            "research_iterations": results["iterations_completed"]
        })

        # Store best sources
        for s in results["sources"][:5]:
            self.memory_bank.store_memory(
                s.get("content", "")[:500],
                "source",
                s.get("relevance_score", 0.5),
                {"url": s.get("url"), "title": s.get("title")}
            )

        self.session_manager.set_agent_output(session_id, "Researcher", results)
        return results

    def _stage_synthesis(self, research_results, query, session_id):
        synthesis = self.synthesizer.synthesize(
            research_results["sources"],
            query,
            session_id
        )

        self.session_manager.update_session(session_id, {
            "current_stage": "validation"
        })

        self.memory_bank.store_memory(
            synthesis["synthesis"],
            "synthesis",
            0.9,
            {"query": query}
        )

        self.session_manager.set_agent_output(session_id, "Synthesizer", synthesis)
        return synthesis

    def _stage_validation(self, synthesis_results, sources, session_id):
        validation = self.validator.validate(
            synthesis_results["synthesis"],
            sources,
            session_id
        )

        self.session_manager.update_session(session_id, {
            "current_stage": "content_generation",
            "validation_results": validation
        })

        self.session_manager.set_agent_output(session_id, "Validator", validation)
        return validation

    def _stage_generation(
        self,
        synthesis_results,
        validation_results,
        sources,
        output_format,
        session_id
    ):
        final_content = self.content_generator.generate(
            synthesis_results["synthesis"],
            validation_results,
            sources,
            output_format,
            session_id
        )

        self.session_manager.update_session(session_id, {
            "current_stage": "completed",
            "status": "completed"
        })

        self.memory_bank.store_memory(
            final_content["content"][:1000],
            "final_content",
            1.0,
            {"format": output_format}
        )

        self.session_manager.set_agent_output(session_id, "ContentGenerator", final_content)
        return final_content


# ================================================================
# HELPER SHORTCUTS
# ================================================================
def quick_research(query: str, format: str = "report"):
    orchestrator = ResearchOrchestrator()
    return orchestrator.conduct_research(query, format)

def get_related_research(query: str, limit: int = 5):
    memory_bank = MemoryBank()
    return memory_bank.get_related_research(query, limit)
