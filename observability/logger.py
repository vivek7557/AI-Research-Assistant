
"""Simple observability helper used by agents for demo purposes."""
import time, threading
from typing import Dict, Any

class _Observability:
    def __init__(self):
        self.session = None
        self.metrics = {}
        self._lock = threading.Lock()

    def start_session(self):
        with self._lock:
            self.session = {'start': time.time(), 'calls': []}

    def end_session(self, status: str = 'completed'):
        with self._lock:
            if self.session is None:
                return
            self.session['end'] = time.time()
            self.session['status'] = status
            duration = self.session['end'] - self.session['start']
            self.metrics['last_session_duration'] = duration

    def observe_agent(self, agent_name: str, op_name: str):
        # context manager stub
        class Ctx:
            def __enter__(selfi):
                selfi.start = time.time()
                return None
            def __exit__(selfi, exc_type, exc, tb):
                pass
        return Ctx()

    def log_llm_call(self, model: str, input_tokens: int, output_tokens: int):
        with self._lock:
            self.session['calls'].append({'model': model, 'in': input_tokens, 'out': output_tokens})

    def get_metrics_summary(self) -> Dict[str, Any]:
        return {'metrics': self.metrics, 'session': self.session}

observability = _Observability()
