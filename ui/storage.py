from pathlib import Path
import json

def read_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def list_json(folder):
    f = Path(folder)
    if not f.exists():
        return []
    return list(sorted(f.glob("*.json")))

