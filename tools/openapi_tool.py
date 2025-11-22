
"""OpenAPI Tool loader and caller.

Usage: load an OpenAPI JSON/YAML file and call operations by operationId.
This is a lightweight helper and does not implement full auth flows.
"""
import os, json, yaml, requests
from typing import Dict, Any, Optional

class OpenAPITool:
    def __init__(self, spec_path: Optional[str] = None):
        self.spec_path = spec_path or os.getenv('OPENAPI_SPEC_PATH')
        self.spec = None
        if self.spec_path:
            with open(self.spec_path, 'r') as f:
                if self.spec_path.lower().endswith(('.yml', '.yaml')):
                    self.spec = yaml.safe_load(f)
                else:
                    self.spec = json.load(f)

    def list_operations(self):
        if not self.spec:
            return []
        ops = []
        paths = self.spec.get('paths', {})
        for path, methods in paths.items():
            for method, meta in methods.items():
                opid = meta.get('operationId') or f"{method}_{path}"
                ops.append({'path': path, 'method': method, 'operationId': opid, 'summary': meta.get('summary')})
        return ops

    def call(self, base_url: str, path: str, method: str = 'get', params: Dict[str, Any] = None, json_body: Dict[str, Any] = None, headers: Dict[str,str] = None):
        url = base_url.rstrip('/') + path
        resp = requests.request(method, url, params=params, json=json_body, headers=headers, timeout=15)
        resp.raise_for_status()
        try:
            return resp.json()
        except Exception:
            return {'text': resp.text}
