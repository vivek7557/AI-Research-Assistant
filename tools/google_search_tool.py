
"""Google Search Tool using Custom Search JSON API or mock fallback.

Requires:
- GOOGLE_API_KEY and GOOGLE_CX (custom search engine id) for real Google Custom Search.
If not provided, it returns mock results for development.
"""
import os
from typing import List, Dict, Any
import requests

class GoogleSearchTool:
    def __init__(self, api_key: str = None, cx: str = None):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.cx = cx or os.getenv('GOOGLE_CX')
        self.base = 'https://www.googleapis.com/customsearch/v1'

    def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        if not self.api_key or not self.cx:
            # Mock fallback
            results = []
            for i in range(max_results):
                results.append({'url': f'https://example.com/{i}', 'title': f'Mock result {i} for {query}', 'content': f'Snippet for {query} #{i}', 'relevance_score': 0.5})
            return {'query': query, 'results': results}

        params = {'key': self.api_key, 'cx': self.cx, 'q': query, 'num': min(max_results,10)}
        resp = requests.get(self.base, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        items = data.get('items', [])
        results = []
        for it in items:
            results.append({
                'url': it.get('link'),
                'title': it.get('title'),
                'content': it.get('snippet'),
                'relevance_score': 1.0
            })
        return {'query': query, 'results': results}
