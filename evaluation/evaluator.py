"""
Agent Evaluation Framework
Evaluates research assistant performance across multiple dimensions
"""
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from loguru import logger
from anthropic import Anthropic
import os


@dataclass
class EvaluationMetrics:
    """Container for evaluation metrics"""
    completeness_score: float  # 0-100
    accuracy_score: float  # 0-100
    relevance_score: float  # 0-100
    quality_score: float  # 0-100
    efficiency_score: float  # 0-100
    citation_score: float  # 0-100
    overall_score: float  # 0-100
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "completeness": self.completeness_score,
            "accuracy": self.accuracy_score,
            "relevance": self.relevance_score,
            "quality": self.quality_score,
            "efficiency": self.efficiency_score,
            "citations": self.citation_score,
            "overall": self.overall_score
        }


class ResearchEvaluator:
    """Evaluates research assistant output quality"""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.evaluation_history: List[Dict[str, Any]] = []
    
    def evaluate_research(
        self,
        query: str,
        results: Dict[str, Any],
        ground_truth: Optional[Dict[str, Any]] = None
    ) -> EvaluationMetrics:
        """
        Comprehensive evaluation of research results
        
        Args:
            query: Original research query
            results: Research assistant output
            ground_truth: Optional reference answers for comparison
        
        Returns:
            EvaluationMetrics with scores
        """
        logger.info(f"Evaluating research for query: {query}")
        
        # Extract components
        synthesis = results.get("synthesis", "")
        validation = results.get("validation", {})
        final_content = results.get("final_content", {}).get("content", "")
        sources = results.get("research_summary", {})
        
        # Run individual evaluations
        completeness = self._evaluate_completeness(query, final_content, sources)
        accuracy = self._evaluate_accuracy(final_content, validation, ground_truth)
        relevance = self._evaluate_relevance(query, final_content)
        quality = self._evaluate_quality(final_content)
        efficiency = self._evaluate_efficiency(results)
        citations = self._evaluate_citations(final_content, sources)
        
        # Calculate overall score (weighted average)
        overall = (
            completeness * 0.20 +
            accuracy * 0.25 +
            relevance * 0.20 +
            quality * 0.15 +
            efficiency * 0.10 +
            citations * 0.10
        )
        
        metrics = EvaluationMetrics(
            completeness_score=completeness,
            accuracy_score=accuracy,
            relevance_score=relevance,
            quality_score=quality,
            efficiency_score=efficiency,
            citation_score=citations,
            overall_score=overall
        )
        
        # Store evaluation
        self.evaluation_history.append({
            "query": query,
            "metrics": metrics.to_dict(),
            "timestamp": time.time()
        })
        
        logger.info(f"Evaluation complete - Overall score: {overall:.1f}")
        return metrics
    
    def _evaluate_completeness(
        self,
        query: str,
        content: str,
        sources: Dict[str, Any]
    ) -> float:
        """Evaluate if research addresses all aspects of the query"""
        system_prompt = """You are an expert evaluator. Assess if the research content completely addresses the query.

Consider:
- Are all aspects of the query covered?
- Is sufficient depth provided?
- Are there obvious gaps?

Return ONLY a JSON with:
{
    "score": 0-100,
    "reasoning": "..."
}"""
        
        user_message = f"""Query: {query}

Content: {content[:2000]}

Source count: {sources.get('total_sources', 0)}

How completely does this content address the query? Score 0-100."""
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            
            result = json.loads(response.content[0].text)
            return float(result.get("score", 70))
        except:
            logger.warning("Completeness evaluation failed, using default")
            return 70.0
    
    def _evaluate_accuracy(
        self,
        content: str,
        validation: Dict[str, Any],
        ground_truth: Optional[Dict[str, Any]]
    ) -> float:
        """Evaluate factual accuracy of content"""
        # Use validation results as primary indicator
        confidence = validation.get("confidence_score", 70)
        
        # Penalty for unverified claims
        unverified = len(validation.get("unverified_claims", []))
        verified = len(validation.get("verified_claims", []))
        
        if verified + unverified > 0:
            verification_ratio = verified / (verified + unverified)
            confidence = confidence * verification_ratio
        
        # Additional penalty for contradictions
        contradictions = len(validation.get("contradictions", []))
        if contradictions > 0:
            confidence -= (contradictions * 5)  # -5 points per contradiction
        
        return max(0, min(100, confidence))
    
    def _evaluate_relevance(self, query: str, content: str) -> float:
        """Evaluate relevance of content to original query"""
        system_prompt = """You are an expert evaluator. Assess how relevant the content is to the query.

Consider:
- Does content directly address the query?
- Is there off-topic information?
- Is the focus appropriate?

Return ONLY a JSON with:
{
    "score": 0-100,
    "reasoning": "..."
}"""
        
        user_message = f"""Query: {query}

Content: {content[:2000]}

How relevant is this content to the query? Score 0-100."""
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            
            result = json.loads(response.content[0].text)
            return float(result.get("score", 75))
        except:
            return 75.0
    
    def _evaluate_quality(self, content: str) -> float:
        """Evaluate writing quality and structure"""
        # Heuristic-based quality assessment
        score = 70.0  # Base score
        
        # Check length (too short or too long is bad)
        word_count = len(content.split())
        if 500 <= word_count <= 3000:
            score += 10
        elif word_count < 200:
            score -= 20
        
        # Check for structure indicators
        structure_indicators = ["introduction", "conclusion", "summary", "##", "###"]
        if any(ind.lower() in content.lower() for ind in structure_indicators):
            score += 10
        
        # Check for paragraphs (at least 3)
        paragraphs = content.split("\n\n")
        if len(paragraphs) >= 3:
            score += 10
        
        return min(100, max(0, score))
    
    def _evaluate_efficiency(self, results: Dict[str, Any]) -> float:
        """Evaluate efficiency of research process"""
        score = 100.0
        
        # Check iteration count (too many iterations = inefficient)
        iterations = results.get("research_summary", {}).get("iterations", 0)
        if iterations > 3:
            score -= (iterations - 3) * 10
        
        # Check source count (too many = unfocused, too few = incomplete)
        sources = results.get("research_summary", {}).get("total_sources", 0)
        if sources < 5:
            score -= 20
        elif sources > 50:
            score -= (sources - 50)
        
        return max(0, min(100, score))
    
    def _evaluate_citations(self, content: str, sources: Dict[str, Any]) -> float:
        """Evaluate proper use of citations"""
        score = 70.0
        
        # Count citation markers [1], [2], etc.
        import re
        citations = re.findall(r'\[\d+\]', content)
        
        if len(citations) > 0:
            score += 20
        
        if len(citations) >= 5:
            score += 10
        
        return min(100, score)
    
    def compare_with_baseline(
        self,
        query: str,
        assistant_results: Dict[str, Any],
        baseline_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare research assistant with baseline (e.g., manual research)"""
        assistant_metrics = self.evaluate_research(query, assistant_results)
        baseline_metrics = self.evaluate_research(query, baseline_results)
        
        comparison = {
            "assistant": assistant_metrics.to_dict(),
            "baseline": baseline_metrics.to_dict(),
            "improvement": {}
        }
        
        # Calculate improvements
        for metric in assistant_metrics.to_dict().keys():
            assistant_score = getattr(assistant_metrics, f"{metric}_score")
            baseline_score = getattr(baseline_metrics, f"{metric}_score")
            improvement = assistant_score - baseline_score
            comparison["improvement"][metric] = improvement
        
        logger.info(f"Comparison complete - Overall improvement: {comparison['improvement']['overall']:.1f}")
        return comparison
    
    def batch_evaluate(
        self,
        test_cases: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate multiple test cases
        
        Args:
            test_cases: List of dicts with 'query' and 'results' keys
        
        Returns:
            Aggregated evaluation results
        """
        all_metrics = []
        
        for i, test_case in enumerate(test_cases):
            logger.info(f"Evaluating test case {i+1}/{len(test_cases)}")
            
            metrics = self.evaluate_research(
                test_case["query"],
                test_case["results"],
                test_case.get("ground_truth")
            )
            
            all_metrics.append(metrics.to_dict())
        
        # Calculate averages
        avg_metrics = {}
        for key in all_metrics[0].keys():
            avg_metrics[f"avg_{key}"] = sum(m[key] for m in all_metrics) / len(all_metrics)
        
        return {
            "num_test_cases": len(test_cases),
            "individual_results": all_metrics,
            "averages": avg_metrics
        }
    
    def get_evaluation_report(self) -> Dict[str, Any]:
        """Generate evaluation report from history"""
        if not self.evaluation_history:
            return {"message": "No evaluations performed yet"}
        
        # Calculate statistics
        all_scores = [e["metrics"]["overall"] for e in self.evaluation_history]
        
        return {
            "total_evaluations": len(self.evaluation_history),
            "average_score": sum(all_scores) / len(all_scores),
            "best_score": max(all_scores),
            "worst_score": min(all_scores),
            "recent_evaluations": self.evaluation_history[-5:]
        }


# Test data generator
def generate_test_cases() -> List[Dict[str, Any]]:
    """Generate sample test cases for evaluation"""
    return [
        {
            "query": "What are the impacts of AI on software engineering jobs?",
            "expected_aspects": ["job displacement", "new opportunities", "skill requirements", "salary changes"]
        },
        {
            "query": "How does climate change affect coral reefs?",
            "expected_aspects": ["ocean warming", "acidification", "bleaching", "biodiversity loss"]
        },
        {
            "query": "What are the benefits and risks of cryptocurrency?",
            "expected_aspects": ["decentralization", "volatility", "security", "regulation"]
        }
    ]
