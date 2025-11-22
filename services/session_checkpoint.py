
"""Session checkpointing service to enable pause/resume of long-running agents.
Stores snapshots to disk (JSON) for simplicity.
"""
import os, json, time
from typing import Dict, Any, Optional

class SessionCheckpointService:
    def __init__(self, storage_dir: str = None):
        self.storage_dir = storage_dir or os.getenv('CHECKPOINT_DIR', './checkpoints')
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_checkpoint(self, session_id: str, state: Dict[str, Any]):
        path = os.path.join(self.storage_dir, f"{session_id}.json")
        payload = {'saved_at': time.time(), 'state': state}
        with open(path, 'w') as f:
            json.dump(payload, f, indent=2)
        return path

    def load_checkpoint(self, session_id: str) -> Optional[Dict[str, Any]]:
        path = os.path.join(self.storage_dir, f"{session_id}.json")
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            payload = json.load(f)
        return payload.get('state')

    def list_checkpoints(self):
        return [f for f in os.listdir(self.storage_dir) if f.endswith('.json')]
