"""
Advanced Research Orchestrator
Multi-agent workflow with:
- Depth control
- Timeline tracking
- Citation support
- Brochure generator mode
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
    ContentGeneratorAgent,
      # NEW agent you added
)

from tools.web_search_tool import WebSearchTool
from memory.memory_bank import SessionManager, MemoryBank, ContextCompactor
from observability.logger import observability
from agents.BrochureAgent import BrochureAgent




class ResearchOrchestrator:
    """Main multi-agent pipeline controller."""

    def __init__(self):
        # Tools
        self.search_tool = WebSearchTool()
        self.brochure_agent = BrochureAgent()


        # Agents
        self.query_planner = QueryPlannerAgent()
        self.researcher = ResearchAgent(self.search_tool)
        self.synthesizer = SynthesisAgent()
        self.validator = ValidationAgent()
        self.content_generator = ContentGeneratorAgent()
        self.brochure_agent = BrochureAgent()       # NEW

        # Memory
        self.session_manager = SessionManager()
        self.memory_bank = MemoryBank()
        self.context_compactor = ContextCompactor()

        # Timeline
        self.timeline: List[Dict[str, Any]] = []

        logger.info("Advanced Research Orchestrator initialized.")


    # ======================================================================
    # MAIN PIPELINE
    # ======================================================================
    def conduct_research(
        self,
        query: str,
        output_format: str = "report",
        session_id: Optional[str] = None,
        depth: int = 3
    ) -> Dict[str, Any]:

        observability.start_session()

        try:
            # -----------------------------
            # SESSION INIT
            # -----------------------------
            if not session_id:
                session_id = f"research_{uuid.uuid4().hex[:8]}"

            self.session_manager.create_session(session_id, query)
            logger.info(f"Starting session {session_id}")

            # -----------------------------
            # DEPTH CONFIG
            # -----------------------------
            depth_config = {
                1: (1, 2),
                2: (2, 3),
                3: (3, 5),
                4: (4, 7),
                5: (6, 10)
            }

            iterations, sources_per_iter = depth_config.get(depth, (3, 5))

            logger.info(f"[DEPTH] depth={depth} → iter={iterations}, sources={sources_per_iter}")

            if hasattr(self.researcher, "set_depth"):
                self.researcher.set_depth(iterations, sources_per_iter)

            # -----------------------------
            # STAGE 1: PLANNING
            # -----------------------------
            plan = self._stage_planning(query, session_id)

            # -----------------------------
            # STAGE 2: RESEARCH LOOP
            # -----------------------------
            research_results = self._stage_research(plan, session_id, iterations)

            # -----------------------------
            # STAGE 3: SYNTHESIS
            # -----------------------------
            synthesis_results = self._stage_synthesis(
                research_results, query, session_id
            )

            # -----------------------------
            # STAGE 4: VALIDATION
            # -----------------------------
            validation_results = self._stage_validation(
                synthesis_results,
                research_results["sources"],
                session_id
            )

            # -----------------------------
            # STAGE 5: CONTENT GENERATION
            # -----------------------------
            if output_format == "brochure":
                final_content = self._stage_brochure(
                    synthesis_results,
                    validation_results,
                    research_results["sources"],
                    session_id
                )
            else:
                final_content = self._stage_generation(
                    synthesis_results,
                    validation_results,
                    research_results["sources"],
                    output_format,
                    session_id
                )

            # -----------------------------
            # FINALIZE SESSION
            # -----------------------------
            session_data = self.session_manager.get_session(session_id)
            session_data["duration"] = time.time() - time.time()

            self.memory_bank.store_research_session(session_data)
            self.session_manager.close_session(session_id, "completed")

            observability.end_session("completed")

            # -----------------------------
            # RETURN RESULT
            # -----------------------------
            return {
                "session_id": session_id,
                "query": query,
                "plan": plan,
                "research_summary": {
                    "total_sources": research_results["total_sources"],
                    "iterations": research_results["iterations_completed"],
                },
                "synthesis": synthesis_results["synthesis"],
                "validation": validation_results,
                "final_content": final_content,
                "metrics": observability.get_metrics_summary(),
                "memory_stats": self.memory_bank.get_statistics(),
                "timeline": self.timeline,
                "depth_used": depth,
            }

        except Exception as e:
            logger.error(f"Research failed: {e}")
            observability.end_session("failed")
            raise



    # ======================================================================
    # STAGE HANDLERS
    # ======================================================================

    def _stage_planning(self, query: str, session_id: str):
        plan = self.query_planner.plan_research(query, session_id)

        self.timeline.append({
            "stage": "Planning",
            "details": "Research plan created.",
            "timestamp": time.time()
        })

        self.session_manager.update_session(session_id, {
            "current_stage": "research",
            "sub_queries": plan.get("sub_questions", [])
        })

        return plan


    def _stage_research(self, plan, session_id, iterations):
        sub_q = plan.get("sub_questions", [])

        results = self.researcher.research(
            sub_q, session_id, self.memory_bank,
            loop_iterations=iterations
        )

        self.timeline.append({
            "stage": "Research",
            "details": f"Completed {iterations} research iterations.",
            "timestamp": time.time()
        })

        self.session_manager.update_session(session_id, {
            "current_stage": "synthesis",
            "sources_found": results["sources"]
        })

        return results


    def _stage_synthesis(self, research_results, query, session_id):
        synthesis = self.synthesizer.synthesize(
            research_results["sources"], query, session_id
        )

        self.timeline.append({
            "stage": "Synthesis",
            "details": "Merged sources into structured synthesis.",
            "timestamp": time.time()
        })

        return synthesis


    def _stage_validation(self, synthesis_results, sources, session_id):
        validation = self.validator.validate(
            synthesis_results["synthesis"], sources, session_id
        )

        self.timeline.append({
            "stage": "Validation",
            "details": "Validated content accuracy and coherence.",
            "timestamp": time.time()
        })

        return validation


    def _stage_generation(self, synthesis_results, validation_results, sources, output_format, session_id):
        final = self.content_generator.generate(
            synthesis_results["synthesis"],
            validation_results,
            sources,
            output_format,
            session_id
        )

        self.timeline.append({
            "stage": "Content Generation",
            "details": f"Generated final {output_format}.",
            "timestamp": time.time()
        })

        return final


    # ======================================================================
    # BROCHURE MODE
    # ======================================================================
    def _stage_brochure(self, synthesis_results, validation_results, sources, session_id):

        pdf_path, pdf_bytes = self.brochure_agent.generate_brochure(
            synthesis_results["synthesis"],
            validation_results,
            sources,
            session_id
        )

        self.timeline.append({
            "stage": "Brochure",
            "details": "Generated brochure PDF.",
            "timestamp": time.time()
        })

        return {
            "content": "Brochure PDF generated.",
            "pdf_path": pdf_path,
            "pdf_bytes": pdf_bytes,
            "word_count": len(synthesis_results["synthesis"].split())
        }



# ======================================================================
# SHORTCUTS
# ======================================================================

def quick_research(query: str, format: str = "report"):
    return ResearchOrchestrator().conduct_research(query, format)

def get_related_research(query: str, limit: int = 5):
    return MemoryBank().get_related_research(query, limit)
