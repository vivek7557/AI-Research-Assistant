
"""Web search tool with TavilyClient wrapper.

This module provides:
- WebSearchTool: search(query, max_results, search_depth)
- CitationFormatter: format_citations(sources, style)

It tries to use TavilyClient if available (recommended). If not available at runtime,
the code will raise a helpful ImportError explaining the need for TAVILY_API_KEY and client.
"""
import os
from typing import List, Dict, Any

try:
    # Recommended official client
    from tavily import TavilyClient
    _HAS_TAVILY = True
except Exception:
    _HAS_TAVILY = False

class WebSearchTool:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise EnvironmentError("TAVILY_API_KEY not set. Set the env var or provide api_key.")
        if not _HAS_TAVILY:
            # Provide helpful error if client missing
            raise ImportError("tavily client library not found. Install the official 'tavily' package or switch to mock mode.")
        self.client = TavilyClient(api_key=self.api_key)

    def search(self, query: str, max_results: int = 5, search_depth: str = "general") -> Dict[str, Any]:
        """Perform a web search using Tavily and return a normalized dict."""
        resp = self.client.search(query=query, max_results=max_results)
        # Normalize response into list of {'url','title','content','relevance_score'}
        results = []
        for item in getattr(resp, 'results', resp.get('results', [])):
            results.append({
                'url': item.get('url') if isinstance(item, dict) else getattr(item, 'url', None),
                'title': item.get('title') if isinstance(item, dict) else getattr(item, 'title', None),
                'content': item.get('snippet') if isinstance(item, dict) else getattr(item, 'snippet', ''),
                'relevance_score': item.get('score', 0.5) if isinstance(item, dict) else getattr(item, 'score', 0.5)
            })
        return {'query': query, 'results': results}

    def search_news(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        return self.search(query + " site:news", max_results=max_results)

    def search_academic(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        return self.search(query + " filetype:pdf", max_results=max_results)

    def rank_results(self, sources: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        # Simple ranking by relevance_score descending
        return sorted(sources, key=lambda s: s.get('relevance_score', 0), reverse=True)


class CitationFormatter:
    @staticmethod
    def format_citations(sources: List[Dict[str, Any]], style: str = "apa") -> List[str]:
        citations = []
        for s in sources:
            title = s.get('title') or 'Untitled'
            url = s.get('url') or ''
            citations.append(f"{title} - {url}")
        return citations
