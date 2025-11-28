"""
Research Orchestrator (FIXED — NO LOGIC CHANGES)
Coordinates all agents.
"""

import uuid
import time
from typing import Dict, Any, Optional, List
from loguru import logger

# Agents
from agents.research_agents import (
    QueryPlannerAgent,
    ResearchAgent,
    SynthesisAgent,
    ValidationAgent,
    ContentGeneratorAgent
)

# Brochure agent (optional)
try:
    from agents.brochure_agent import BrochureAgent
    BROCHURE_AVAILABLE = True
except:
    BROCHURE_AVAILABLE = False

# Memory + tools
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

        # Optional agent
        self.brochure_agent = BrochureAgent() if BROCHURE_AVAILABLE else None

        # Memory
        self.session_manager = SessionManager()
        self.memory_bank = MemoryBank()
        self.context_compactor = ContextCompactor()

        # timeline for UI
        self.timeline = []

        logger.info("Research Orchestrator initialized.")


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
            # Create session
            if not session_id:
                session_id = f"research_{uuid.uuid4().hex[:8]}"
            self.session_manager.create_session(session_id, query)

            logger.info(f"Starting session {session_id}")

            # DEPTH CONFIG
            depth_config = {
                1: (1, 2),   # ultra fast
                2: (2, 3),   # fast
                3: (3, 5),   # normal
                4: (4, 7),   # deep
                5: (6, 10),  # ultra deep
            }

            iterations, sources_per_iter = depth_config.get(depth, (3, 5))
            self.researcher.set_depth(iterations, sources_per_iter)

            logger.info(f"Depth={depth} iterations={iterations} sources={sources_per_iter}")

            # -----------------------------------------------------
            # STAGE 1 – PLANNING
            # -----------------------------------------------------
            plan = self._stage_planning(query, session_id)

            # -----------------------------------------------------
            # STAGE 2 – RESEARCH LOOP
            # -----------------------------------------------------
            research_results = self._stage_research(plan, session_id, iterations)

            # -----------------------------------------------------
            # STAGE 3 – SYNTHESIS
            # -----------------------------------------------------
            synthesis_results = self._stage_synthesis(
                research_results,
                query,
                session_id
            )

            # -----------------------------------------------------
            # STAGE 4 – VALIDATION
            # -----------------------------------------------------
            validation_results = self._stage_validation(
                synthesis_results,
                research_results["sources"],
                session_id
            )

            # -----------------------------------------------------
            # BROCHURE MODE (only if output_format == "brochure")
            # -----------------------------------------------------
            brochure_output = None
            if output_format.lower() == "brochure" and self.brochure_agent:
                brochure_output = self._stage_brochure(
                    synthesis_results,
                    validation_results,
                    research_results["sources"],
                    session_id
                )

            # -----------------------------------------------------
            # STAGE 5 – FINAL CONTENT
            # -----------------------------------------------------
            final_content = self._stage_generation(
                synthesis_results,
                validation_results,
                research_results["sources"],
                output_format,
                session_id
            )

            # Finalize session
            session_data = self.session_manager.get_session(session_id)
            session_data["duration"] = time.time() - time.mktime(
                time.strptime(session_data["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            )

            self.memory_bank.store_research_session(session_data)
            self.session_manager.close_session(session_id, "completed")
            observability.end_session("completed")

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
                "brochure": brochure_output,         # optional
                "metrics": observability.get_metrics_summary(),
                "memory_stats": self.memory_bank.get_statistics(),
                "depth_used": depth,
                "timeline": self.timeline
            }

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            observability.end_session("failed")
            raise


    # =====================================================================
    # INDIVIDUAL STAGES
    # =====================================================================

    def _stage_planning(self, query: str, session_id: str):
        self.timeline.append({"stage": "Planning", "timestamp": time.time()})

        plan = self.query_planner.plan_research(query, session_id)

        self.session_manager.update_session(
            session_id,
            {"current_stage": "research", "sub_queries": plan.get("sub_questions", [])}
        )

        return plan


    def _stage_research(self, plan, session_id, iterations):
        self.timeline.append({"stage": "Research Loop", "timestamp": time.time()})

        return self.researcher.research(
            plan.get("sub_questions", []),
            session_id,
            self.memory_bank,
            loop_iterations=iterations
        )


    def _stage_synthesis(self, research_results, query, session_id):
        self.timeline.append({"stage": "Synthesis", "timestamp": time.time()})

        return self.synthesizer.synthesize(
            research_results["sources"],
            query,
            session_id
        )


    def _stage_validation(self, synthesis_results, sources, session_id):
        self.timeline.append({"stage": "Validation", "timestamp": time.time()})

        return self.validator.validate(
            synthesis_results["synthesis"],
            sources,
            session_id
        )


    # ---------------------------------------------------------------------
    # BROCHURE MODE (optional)
    # ---------------------------------------------------------------------
    def _stage_brochure(self, synthesis_results, validation_results, sources, session_id):

        self.timeline.append({"stage": "Brochure", "timestamp": time.time()})

        if not self.brochure_agent:
            return None

        brochure = self.brochure_agent.generate(
            title="Research Brochure",
            sections={
                "Summary": synthesis_results["synthesis"][:1500],
                "Validation": str(validation_results)
            },
            sources=sources
        )

        return brochure


    def _stage_generation(
        self,
        synthesis_results,
        validation_results,
        sources,
        output_format,
        session_id
    ):
        self.timeline.append({"stage": "Final Content", "timestamp": time.time()})

        return self.content_generator.generate(
            synthesis_results["synthesis"],
            validation_results,
            sources,
            output_format,
            session_id
        )


