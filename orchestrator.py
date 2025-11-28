"""
Research Orchestrator
Coordinates all agents in a sequential + loop-based workflow
"""

import uuid
import time
from typing import Dict, Any, Optional, List
from loguru import logger

from agents.research_agents import (
    QueryPlannerAgent,
    ResearchAgent,
    SynthesisAgent,
    ValidationAgent,
    ContentGeneratorAgent
)

from agents.BrochureAgent import BrochureAgent  # NEW SAFE IMPORT
from tools.web_search_tool import WebSearchTool
from memory.memory_bank import SessionManager, MemoryBank, ContextCompactor
from observability.logger import observability



class ResearchOrchestrator:

    def __init__(self):
        # Tools
        self.search_tool = WebSearchTool()

        # Agents
        self.query_planner = QueryPlannerAgent()
        self.researcher = ResearchAgent(self.search_tool)
        self.synthesizer = SynthesisAgent()
        self.validator = ValidationAgent()
        self.content_generator = ContentGeneratorAgent()

        # Optional Brochure Agent
        self.brochure_agent = BrochureAgent()

        # Memory
        self.session_manager = SessionManager()
        self.memory_bank = MemoryBank()
        self.context_compactor = ContextCompactor()

        logger.info("Research Orchestrator initialized")


    # =====================================================================
    # MAIN PIPELINE
    # =====================================================================
    def conduct_research(
        self,
        query: str,
        output_format: str = "report",
        session_id: Optional[str] = None,
        depth: int = 3
    ) -> Dict[str, Any]:

        observability.start_session()

        try:
            # SESSION INIT
            if not session_id:
                session_id = f"research_{uuid.uuid4().hex[:8]}"

            self.session_manager.create_session(session_id, query)
            logger.info(f"Starting research session: {session_id}")

            # DEPTH SETTINGS
            depth_config = {
                1: (1, 2),
                2: (2, 3),
                3: (3, 5),
                4: (4, 7),
                5: (6, 10)
            }

            iterations, sources_per_iter = depth_config.get(depth, (3, 5))

            logger.info(
                f"[DEPTH CONFIG] depth={depth} → "
                f"iterations={iterations}, sources_per_iter={sources_per_iter}"
            )

            if hasattr(self.researcher, "set_depth"):
                self.researcher.set_depth(iterations, sources_per_iter)

            # ======================================================
            # STAGE 1 — Planning
            # ======================================================
            plan = self._stage_planning(query, session_id)

            # ======================================================
            # STAGE 2 — Research Loop
            # ======================================================
            research_results = self._stage_research(plan, session_id, iterations)

            # ======================================================
            # STAGE 3 — Synthesis
            # ======================================================
            synthesis_results = self._stage_synthesis(
                research_results,
                query,
                session_id
            )

            # ======================================================
            # STAGE 4 — Validation
            # ======================================================
            validation_results = self._stage_validation(
                synthesis_results,
                research_results["sources"],
                session_id
            )

            # ======================================================
            # STAGE 5 — Final Content Generation
            # ======================================================
            final_content = self._stage_generation(
                synthesis_results,
                validation_results,
                research_results["sources"],
                output_format,
                session_id
            )

            # Optional Brochure
            try:
                brochure = self.brochure_agent.generate(
                    title=f"Brochure: {query}",
                    sections={
                        "Overview": synthesis_results["synthesis"],
                        "Key Findings": validation_results.get("key_points", "")
                    },
                    sources=research_results["sources"]
                )
            except Exception:
                brochure = None

            # === Final Session Save ===
            session_data = self.session_manager.get_session(session_id)
            session_data["duration"] = time.time() - time.mktime(
                time.strptime(session_data["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            )

            self.memory_bank.store_research_session(session_data)
            self.session_manager.close_session(session_id, "completed")
            observability.end_session("completed")

            # Return final result bundle
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
                "sources": research_results["sources"],
                "brochure": brochure,
                "metrics": observability.get_metrics_summary(),
                "memory_stats": self.memory_bank.get_statistics(),
                "depth_used": depth
            }

        except Exception as e:
            logger.error(f"Research failed: {str(e)}")
            observability.end_session("failed")
            raise



    # =====================================================================
    # STAGE HANDLERS
    # =====================================================================

    def _stage_planning(self, query, session_id):
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

        return plan


    def _stage_research(self, plan, session_id, iterations):
        sub_questions = plan.get("sub_questions", [])

        results = self.researcher.research(
            sub_questions,
            session_id,
            self.memory_bank,
            loop_iterations=iterations
        )

        self.session_manager.update_session(session_id, {
            "current_stage": "synthesis",
            "sources_found": results["sources"],
            "research_iterations": results["iterations_completed"]
        })

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

        return synthesis


    def _stage_validation(self, synthesis_results, sources, session_id):
        validation = self.validator.validate(
            synthesis_results["synthesis"],
            sources,
            session_id
        )

        self.session_manager.update_session(session_id, {
            "current_stage": "content_generation"
        })

        return validation


    def _stage_generation(
        self,
        synthesis_results,
        validation_results,
        sources,
        output_format,
        session_id
    ):
        return self.content_generator.generate(
            synthesis_results["synthesis"],
            validation_results,
            sources,
            output_format,
            session_id
        )
