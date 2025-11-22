
"""
API Server for AI Research Assistant Enterprise
"""
import os
import asyncio
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn
from datetime import datetime
import uuid

from orchestrator import ResearchOrchestrator
from services.session_checkpoint import SessionCheckpointService
from evaluation.evaluator import ResearchEvaluator
from memory.memory_bank import MemoryBank

# Initialize FastAPI app
app = FastAPI(
    title="AI Research Assistant Enterprise",
    description="Enterprise-grade AI research assistant with multi-agent system",
    version="1.0.0"
)

# Initialize components
orchestrator = ResearchOrchestrator()
checkpoint_service = SessionCheckpointService()
evaluator = ResearchEvaluator()
memory_bank = MemoryBank()

# Pydantic models
class ResearchRequest(BaseModel):
    query: str
    max_sources: int = 5
    include_citations: bool = True
    max_iterations: int = 3
    output_format: str = "report"

class ResearchResponse(BaseModel):
    session_id: str
    status: str
    result: Optional[Dict] = None
    error: Optional[str] = None
    created_at: datetime

class ResearchStatus(BaseModel):
    session_id: str
    status: str
    progress: float
    result: Optional[Dict] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Store for research tasks (in production, use Redis or database)
research_tasks: Dict[str, dict] = {}

@app.get("/")
async def root():
    return {
        "message": "AI Research Assistant Enterprise API",
        "status": "running",
        "endpoints": {
            "submit": "/research",
            "status": "/research/{session_id}",
            "list": "/research",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.post("/research", response_model=ResearchResponse)
async def submit_research_task(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Submit a new research task"""
    try:
        # Create a new session
        session_id = f"research_{uuid.uuid4().hex[:8]}"
        
        # Store initial task info
        research_tasks[session_id] = {
            "session_id": session_id,
            "status": "pending",
            "progress": 0.0,
            "query": request.query,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Start research in background
        background_tasks.add_task(
            run_research_task,
            session_id,
            request.query,
            request.max_sources,
            request.include_citations,
            request.max_iterations,
            request.output_format
        )
        
        response = ResearchResponse(
            session_id=session_id,
            status="pending",
            created_at=research_tasks[session_id]["created_at"]
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def run_research_task(session_id: str, query: str, max_sources: int, include_citations: bool, max_iterations: int, output_format: str):
    """Run the research task in background"""
    try:
        # Update status to running
        research_tasks[session_id].update({
            "status": "running",
            "progress": 0.1,
            "updated_at": datetime.now()
        })
        
        # Run the research
        result = orchestrator.conduct_research(
            query=query,
            max_sources=max_sources,
            include_citations=include_citations,
            max_iterations=max_iterations,
            output_format=output_format,
            session_id=session_id
        )
        
        # Update status to completed
        research_tasks[session_id].update({
            "status": "completed",
            "progress": 1.0,
            "result": result,
            "updated_at": datetime.now()
        })
        
        # Save checkpoint
        checkpoint_service.save_checkpoint(session_id, result)
        
    except Exception as e:
        # Update status to error
        research_tasks[session_id].update({
            "status": "error",
            "error": str(e),
            "updated_at": datetime.now()
        })

@app.get("/research/{session_id}", response_model=ResearchStatus)
async def get_research_status(session_id: str):
    """Get the status of a research task"""
    if session_id not in research_tasks:
        raise HTTPException(status_code=404, detail="Research task not found")
    
    task = research_tasks[session_id]
    return ResearchStatus(
        session_id=task["session_id"],
        status=task["status"],
        progress=task.get("progress", 0.0),
        result=task.get("result"),
        error=task.get("error"),
        created_at=task["created_at"],
        updated_at=task["updated_at"]
    )

@app.get("/research", response_model=List[ResearchStatus])
async def get_all_research_tasks():
    """Get all research tasks"""
    tasks = []
    for task_data in research_tasks.values():
        tasks.append(ResearchStatus(
            session_id=task_data["session_id"],
            status=task_data["status"],
            progress=task_data.get("progress", 0.0),
            result=task_data.get("result"),
            error=task_data.get("error"),
            created_at=task_data["created_at"],
            updated_at=task_data["updated_at"]
        ))
    return tasks

@app.post("/evaluate/{session_id}")
async def evaluate_research(session_id: str):
    """Evaluate the quality of research results"""
    if session_id not in research_tasks:
        raise HTTPException(status_code=404, detail="Research task not found")
    
    task = research_tasks[session_id]
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Research task not completed")
    
    result = task.get("result")
    if not result:
        raise HTTPException(status_code=400, detail="No results to evaluate")
    
    # Perform evaluation
    evaluation = evaluator.evaluate_research(task["query"], result)
    
    return {
        "session_id": session_id,
        "evaluation": evaluation
    }

@app.get("/memory/stats")
async def get_memory_stats():
    """Get memory bank statistics"""
    stats = memory_bank.get_stats()
    return stats

@app.get("/memory/related")
async def get_related_research(query: str, limit: int = 5):
    """Find related research in memory bank"""
    related = memory_bank.find_similar(query, limit=limit)
    return related

# Legacy endpoints for backward compatibility
@app.post('/run')
def run(req: ResearchRequest):
    if not req.query:
        raise HTTPException(status_code=400, detail='query required')
    session_id = f"research_{uuid.uuid4().hex[:8]}"
    # Start research synchronously (could be background task)
    results = orchestrator.conduct_research(
        req.query, 
        output_format=req.output_format, 
        session_id=session_id,
        max_sources=req.max_sources,
        include_citations=req.include_citations,
        max_iterations=req.max_iterations
    )
    # Save checkpoint snapshot (simple state)
    checkpoint_service.save_checkpoint(session_id, results)
    return {'session_id': session_id, 'summary': results.get('research_summary', {})}

@app.get('/resume/{session_id}')
def resume(session_id: str):
    state = checkpoint_service.load_checkpoint(session_id)
    if not state:
        raise HTTPException(status_code=404, detail='checkpoint not found')
    return {'session_id': session_id, 'state_preview': state.get('query', 'no query')}
