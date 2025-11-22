
"""Prometheus metrics exporter stub for development."""
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

LLM_CALLS = Counter('llm_calls_total', 'Total LLM calls')
SESSIONS = Counter('research_sessions_total', 'Total research sessions')
LAST_SESSION_DURATION = Gauge('last_session_duration_seconds', 'Last session duration seconds')

def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
