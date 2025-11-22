"""
Parallel Agent Implementation
Enables simultaneous research on multiple sub-questions
"""
import asyncio
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
from observability.logger import observability
from tools.web_search_tool import WebSearchTool
from memory.memory_bank import MemoryBank


class ParallelResearchCoordinator:
    """
    Coordinates parallel research agents
    Multiple agents work simultaneously on different sub-questions
    """
    
    def __init__(self, search_tool: WebSearchTool, max_workers: int = 3):
        self.search_tool = search_tool
        self.max_workers = max_workers
        logger.info(f"Initialized ParallelResearchCoordinator with {max_workers} workers")
    
    def parallel_research(
        self,
        sub_questions: List[Dict[str, Any]],
        session_id: str,
        memory_bank: MemoryBank
    ) -> Dict[str, Any]:
        """
        Execute parallel research on multiple sub-questions
        
        Args:
            sub_questions: List of sub-questions to research
            session_id: Current session ID
            memory_bank: Memory bank for storing results
        
        Returns:
            Combined research results from all parallel agents
        """
        with observability.observe_agent("ParallelResearcher", "parallel_research") as span_id:
            logger.info(f"Starting parallel research on {len(sub_questions)} sub-questions")
            
            all_sources = []
            research_log = []
            
            # Execute searches in parallel using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all sub-questions for parallel processing
                future_to_question = {
                    executor.submit(
                        self._research_single_question,
                        sq,
                        session_id,
                        memory_bank
                    ): sq for sq in sub_questions
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_question):
                    question = future_to_question[future]
                    try:
                        result = future.result()
                        all_sources.extend(result['sources'])
                        research_log.append({
                            'question': question['question'],
                            'sources_found': len(result['sources']),
                            'status': 'completed'
                        })
                        logger.info(f"✓ Completed: {question['question'][:50]}...")
                        
                    except Exception as e:
                        logger.error(f"✗ Failed: {question['question'][:50]}... - {str(e)}")
                        research_log.append({
                            'question': question['question'],
                            'sources_found': 0,
                            'status': 'failed',
                            'error': str(e)
                        })
            
            # Rank all sources by relevance
            ranked_sources = self.search_tool.rank_results(
                all_sources,
                " ".join([sq['question'] for sq in sub_questions])
            )
            
            logger.info(f"Parallel research complete: {len(ranked_sources)} total sources")
            
            return {
                'sources': ranked_sources,
                'research_log': research_log,
                'total_sources': len(ranked_sources),
                'parallel_workers': self.max_workers,
                'sub_questions_processed': len(sub_questions)
            }
    
    def _research_single_question(
        self,
        sub_question: Dict[str, Any],
        session_id: str,
        memory_bank: MemoryBank
    ) -> Dict[str, Any]:
        """
        Research a single sub-question (executed in parallel)
        
        Args:
            sub_question: Single sub-question to research
            session_id: Current session ID
            memory_bank: Memory bank for storing
        
        Returns:
            Research results for this sub-question
        """
        question = sub_question['question']
        strategy = sub_question.get('search_strategy', 'general')
        
        logger.debug(f"Researching: {question}")
        
        # Execute search based on strategy
        if strategy == 'academic':
            result = self.search_tool.search_academic(question, max_results=5)
        elif strategy == 'news':
            result = self.search_tool.search_news(question, max_results=5)
        else:
            result = self.search_tool.search(
                question,
                max_results=5,
                search_depth='advanced'
            )
        
        sources = result.get('results', [])
        
        # Store sources in memory bank
        for source in sources:
            memory_bank.store_source(
                url=source.get('url', ''),
                title=source.get('title', ''),
                content=source.get('content', ''),
                relevance=source.get('relevance_score', 0.5),
                metadata={
                    'sub_question': question,
                    'strategy': strategy,
                    'session_id': session_id
                }
            )
        
        return {
            'question': question,
            'sources': sources,
            'strategy': strategy
        }


class AsyncParallelResearchCoordinator:
    """
    Async version using asyncio for even better parallelization
    """
    
    def __init__(self, search_tool: WebSearchTool):
        self.search_tool = search_tool
        logger.info("Initialized AsyncParallelResearchCoordinator")
    
    async def parallel_research_async(
        self,
        sub_questions: List[Dict[str, Any]],
        session_id: str,
        memory_bank: MemoryBank
    ) -> Dict[str, Any]:
        """
        Execute async parallel research on multiple sub-questions
        
        Even more efficient than thread-based parallelism
        """
        logger.info(f"Starting async parallel research on {len(sub_questions)} sub-questions")
        
        # Create tasks for all sub-questions
        tasks = [
            self._research_single_question_async(sq, session_id, memory_bank)
            for sq in sub_questions
        ]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        all_sources = []
        research_log = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Task {i} failed: {str(result)}")
                research_log.append({
                    'question': sub_questions[i]['question'],
                    'status': 'failed',
                    'error': str(result)
                })
            else:
                all_sources.extend(result['sources'])
                research_log.append({
                    'question': result['question'],
                    'sources_found': len(result['sources']),
                    'status': 'completed'
                })
        
        # Rank results
        ranked_sources = self.search_tool.rank_results(
            all_sources,
            " ".join([sq['question'] for sq in sub_questions])
        )
        
        logger.info(f"Async parallel research complete: {len(ranked_sources)} sources")
        
        return {
            'sources': ranked_sources,
            'research_log': research_log,
            'total_sources': len(ranked_sources),
            'execution_mode': 'async',
            'sub_questions_processed': len(sub_questions)
        }
    
    async def _research_single_question_async(
        self,
        sub_question: Dict[str, Any],
        session_id: str,
        memory_bank: MemoryBank
    ) -> Dict[str, Any]:
        """Async version of single question research"""
        question = sub_question['question']
        strategy = sub_question.get('search_strategy', 'general')
        
        # Wrap sync search in async
        loop = asyncio.get_event_loop()
        
        if strategy == 'academic':
            result = await loop.run_in_executor(
                None,
                self.search_tool.search_academic,
                question,
                5
            )
        elif strategy == 'news':
            result = await loop.run_in_executor(
                None,
                self.search_tool.search_news,
                question,
                5
            )
        else:
            result = await loop.run_in_executor(
                None,
                lambda: self.search_tool.search(question, max_results=5, search_depth='advanced')
            )
        
        sources = result.get('results', [])
        
        # Store in memory bank
        for source in sources:
            memory_bank.store_source(
                url=source.get('url', ''),
                title=source.get('title', ''),
                content=source.get('content', ''),
                relevance=source.get('relevance_score', 0.5),
                metadata={
                    'sub_question': question,
                    'strategy': strategy,
                    'session_id': session_id,
                    'execution': 'async'
                }
            )
        
        return {
            'question': question,
            'sources': sources,
            'strategy': strategy
        }


# Comparison demo
def demo_parallel_vs_sequential():
    """
    Demonstrate speed improvement of parallel vs sequential research
    """
    import time
    from tools.web_search_tool import WebSearchTool
    from memory.memory_bank import MemoryBank
    
    search_tool = WebSearchTool()
    memory_bank = MemoryBank()
    
    sub_questions = [
        {'question': 'What is artificial intelligence?', 'strategy': 'general'},
        {'question': 'How does machine learning work?', 'strategy': 'academic'},
        {'question': 'Latest AI news 2024', 'strategy': 'news'},
        {'question': 'AI ethics concerns', 'strategy': 'general'},
    ]
    
    # Sequential execution
    print("Sequential Execution:")
    start = time.time()
    for sq in sub_questions:
        search_tool.search(sq['question'], max_results=3)
    sequential_time = time.time() - start
    print(f"Time: {sequential_time:.2f}s\n")
    
    # Parallel execution
    print("Parallel Execution:")
    coordinator = ParallelResearchCoordinator(search_tool, max_workers=4)
    start = time.time()
    coordinator.parallel_research(sub_questions, "demo_session", memory_bank)
    parallel_time = time.time() - start
    print(f"Time: {parallel_time:.2f}s\n")
    
    # Show improvement
    speedup = sequential_time / parallel_time
    print(f"Speedup: {speedup:.2f}x faster with parallel execution!")
    print(f"Time saved: {sequential_time - parallel_time:.2f}s")


if __name__ == "__main__":
    demo_parallel_vs_sequential()
