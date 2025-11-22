
"""Simple in-memory MemoryBank and SessionManager for development/testing."""
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

class MemoryBank:
    def __init__(self):
        self.memories: List[Dict[str, Any]] = []

    def store_memory(self, content: str, category: str = "general", importance: float = 0.5, metadata: dict = None):
        entry = {
            'id': len(self.memories) + 1,
            'content': content,
            'category': category,
            'importance': importance,
            'metadata': metadata or {},
            'created_at': time.time()
        }
        self.memories.append(entry)
        return entry

    def store_source(self, url: str, title: str, content: str, relevance: float = 0.5, metadata: dict = None):
        return self.store_memory(content=content, category='source', importance=relevance, metadata={'url': url, 'title': title, **(metadata or {})})

    def store_research_session(self, session_data: dict):
        return self.store_memory(content=str(session_data)[:1000], category='session', importance=1.0, metadata={'session': session_data})

    def get_statistics(self) -> Dict[str, Any]:
        total = len(self.memories)
        avg_imp = sum(m.get('importance',0) for m in self.memories)/total if total else 0
        return {
            'total_memories': total,
            'avg_importance': avg_imp,
            'completed_sessions': len([m for m in self.memories if m.get('category')=='session']),
            'total_sources': len([m for m in self.memories if m.get('category')=='source'])
        }

    def get_related_research(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        # naive substring match in content
        matches = [m for m in self.memories if query.lower() in (m.get('content') or '').lower()]
        return matches[:limit]


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, session_id: str, query: str):
        self.sessions[session_id] = {
            'id': session_id,
            'query': query,
            'created_at': datetime.utcnow().isoformat(),
            'current_stage': 'planning',
            'outputs': {}
        }
        return self.sessions[session_id]

    def update_session(self, session_id: str, data: dict):
        if session_id in self.sessions:
            self.sessions[session_id].update(data)
            return self.sessions[session_id]
        raise KeyError('Session not found')

    def get_session(self, session_id: str):
        return self.sessions.get(session_id)

    def set_agent_output(self, session_id: str, agent_name: str, output: Any):
        if session_id in self.sessions:
            self.sessions[session_id]['outputs'][agent_name] = output

    def close_session(self, session_id: str, status: str = 'completed'):
        if session_id in self.sessions:
            self.sessions[session_id]['status'] = status
            self.sessions[session_id]['closed_at'] = time.time()
            return self.sessions[session_id]
        raise KeyError('Session not found')


class ContextCompactor:
    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens

    def compact_sources(self, sources: List[Dict[str, Any]], target_tokens: int = 1000):
        # naive compaction - truncate content fields
        compacted = []
        for s in sources:
            c = dict(s)
            content = c.get('content') or ''
            c['content'] = content[:min(2000, len(content))]
            compacted.append(c)
        return compacted
