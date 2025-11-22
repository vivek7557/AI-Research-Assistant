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
    Orchestrates the multi-agent research pipeline
    
    Architecture:
    QueryPlanner -> ResearchAgent (loop) -> Synthesizer -> Validator -> ContentGenerator
                    (sequential)           (loop)        (sequential)
    """
    
    def __init__(self):
        # Initialize tools
        self.search_tool = WebSearchTool()
        
        # Initialize agents
        self.query_planner = QueryPlannerAgent()
        self.researcher = ResearchAgent(self.search_tool)
        self.synthesizer = SynthesisAgent()
        self.validator = ValidationAgent()
        self.content_generator = ContentGeneratorAgent()
        
        # Initialize memory
        self.session_manager = SessionManager()
        self.memory_bank = MemoryBank()
        self.context_compactor = ContextCompactor()
        
        logger.info("Research Orchestrator initialized")
    
    def conduct_research(
        self,
        query: str,
        output_format: str = "report",
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main research workflow
        
        Args:
            query: Research question/topic
            output_format: Desired output format (report/article/summary/presentation)
            session_id: Optional session ID for resuming
        
        Returns:
            Complete research results with generated content
        """
        # Start observability
        observability.start_session()
        
        try:
            # Create or resume session
            if not session_id:
                session_id = f"research_{uuid.uuid4().hex[:8]}"
            
            self.session_manager.create_session(session_id, query)
            logger.info(f"Starting research session: {session_id}")
            
            # STAGE 1: Query Planning (Sequential Agent)
            logger.info("STAGE 1: Query Planning")
            plan = self._stage_planning(query, session_id)
            
            # STAGE 2: Research (Loop Agent)
            logger.info("STAGE 2: Research Loop")
            research_results = self._stage_research(plan, session_id)
            
            # STAGE 3: Synthesis (Sequential Agent)
            logger.info("STAGE 3: Synthesis")
            synthesis_results = self._stage_synthesis(research_results, query, session_id)
            
            # STAGE 4: Validation (Sequential Agent)
            logger.info("STAGE 4: Validation")
            validation_results = self._stage_validation(
                synthesis_results,
                research_results["sources"],
                session_id
            )
            
            # STAGE 5: Content Generation (Sequential Agent)
            logger.info("STAGE 5: Content Generation")
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
            
            # Store in memory bank
            self.memory_bank.store_research_session(session_data)
            self.session_manager.close_session(session_id, "completed")
            
            # Complete observability
            observability.end_session("completed")
            
            # Compile final results
            results = {
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
                "memory_stats": self.memory_bank.get_statistics()
            }
            
            logger.info(f"Research completed successfully: {session_id}")
            return results
            
        except Exception as e:
            logger.error(f"Research failed: {str(e)}")
            observability.end_session("failed")
            raise
    
    def _stage_planning(self, query: str, session_id: str) -> Dict[str, Any]:
        """Stage 1: Planning with QueryPlannerAgent"""
        plan = self.query_planner.plan_research(query, session_id)
        
        # Update session
        self.session_manager.update_session(session_id, {
            "current_stage": "research",
            "sub_queries": plan.get("sub_questions", [])
        })
        
        # Store in memory
        self.memory_bank.store_memory(
            content=f"Research plan for: {query}",
            category="planning",
            importance=0.8,
            metadata={"plan": plan, "session_id": session_id}
        )
        
        self.session_manager.set_agent_output(session_id, "QueryPlanner", plan)
        return plan
    
    def _stage_research(self, plan: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Stage 2: Iterative research with ResearchAgent (Loop Agent)"""
        sub_questions = plan.get("sub_questions", [])
        
        # Execute research loop
        research_results = self.researcher.research(
            sub_questions,
            session_id,
            self.memory_bank
        )
        
        # Update session
        self.session_manager.update_session(session_id, {
            "current_stage": "synthesis",
            "sources_found": research_results["sources"],
            "research_iterations": research_results["iterations_completed"]
        })
        
        # Store key insights in memory
        for source in research_results["sources"][:5]:  # Top 5 sources
            self.memory_bank.store_memory(
                content=source.get("content", "")[:500],
                category="source",
                importance=source.get("relevance_score", 0.5),
                metadata={
                    "url": source.get("url", ""),
                    "title": source.get("title", ""),
                    "session_id": session_id
                }
            )
        
        self.session_manager.set_agent_output(session_id, "Researcher", research_results)
        return research_results
    
    def _stage_synthesis(
        self,
        research_results: Dict[str, Any],
        query: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Stage 3: Synthesis with SynthesisAgent"""
        synthesis_results = self.synthesizer.synthesize(
            research_results["sources"],
            query,
            session_id
        )
        
        # Update session
        self.session_manager.update_session(session_id, {
            "current_stage": "validation"
        })
        
        # Store synthesis in memory
        self.memory_bank.store_memory(
            content=synthesis_results["synthesis"],
            category="synthesis",
            importance=0.9,
            metadata={"session_id": session_id, "query": query}
        )
        
        self.session_manager.set_agent_output(session_id, "Synthesizer", synthesis_results)
        return synthesis_results
    
    def _stage_validation(
        self,
        synthesis_results: Dict[str, Any],
        sources: List[Dict[str, Any]],
        session_id: str
    ) -> Dict[str, Any]:
        """Stage 4: Validation with ValidationAgent"""
        validation_results = self.validator.validate(
            synthesis_results["synthesis"],
            sources,
            session_id
        )
        
        # Update session
        self.session_manager.update_session(session_id, {
            "current_stage": "content_generation",
            "validation_results": validation_results
        })
        
        # Store validation in memory if issues found
        if validation_results.get("gaps") or validation_results.get("contradictions"):
            self.memory_bank.store_memory(
                content=f"Validation issues: {validation_results}",
                category="validation",
                importance=0.7,
                metadata={"session_id": session_id}
            )
        
        self.session_manager.set_agent_output(session_id, "Validator", validation_results)
        return validation_results
    
    def _stage_generation(
        self,
        synthesis_results: Dict[str, Any],
        validation_results: Dict[str, Any],
        sources: List[Dict[str, Any]],
        output_format: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Stage 5: Content generation with ContentGeneratorAgent"""
        final_content = self.content_generator.generate(
            synthesis_results["synthesis"],
            validation_results,
            sources,
            output_format,
            session_id
        )
        
        # Update session
        self.session_manager.update_session(session_id, {
            "current_stage": "completed",
            "status": "completed"
        })
        
        # Store final content in memory
        self.memory_bank.store_memory(
            content=final_content["content"][:1000],  # Store excerpt
            category="final_content",
            importance=1.0,
            metadata={
                "session_id": session_id,
                "format": output_format,
                "word_count": final_content["word_count"]
            }
        )
        
        self.session_manager.set_agent_output(session_id, "ContentGenerator", final_content)
        return final_content
    
    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a research session"""
        return self.session_manager.get_session(session_id)
    
    def resume_session(self, session_id: str) -> Dict[str, Any]:
        """Resume a paused/failed research session"""
        session = self.session_manager.get_session(session_id)
        
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        logger.info(f"Resuming session {session_id} from stage: {session['current_stage']}")
        
        # Get original query
        query = session["query"]
        
        # Determine where to resume based on current stage
        current_stage = session["current_stage"]
        
        if current_stage == "completed":
            logger.info("Session already completed")
            return self.session_manager.get_session(session_id)
        
        # Resume from the current stage
        # This is a simplified version - in production, you'd have more sophisticated resume logic
        logger.warning("Full resume logic not implemented - restarting research")
        return self.conduct_research(query, session_id=session_id)


# Convenience functions
def quick_research(query: str, format: str = "report") -> Dict[str, Any]:
    """Quick research function for simple use"""
    orchestrator = ResearchOrchestrator()
    return orchestrator.conduct_research(query, format)


def get_related_research(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Get related past research from memory bank"""
    memory_bank = MemoryBank()
    return memory_bank.get_related_research(query, limit)
