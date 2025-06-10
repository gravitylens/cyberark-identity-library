import os
import sys
import types
from pathlib import Path

# Load environment variables from a local .env file if present
env_path = Path('.env')
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip())

# Provide a simple stub for the requests module if it's missing.
if 'requests' not in sys.modules:
    requests_stub = types.ModuleType('requests')

    class Response:
        def __init__(self, data=None):
            self._data = data or {
                "success": True,
                "Result": {"id": "dummy"},
                "access_token": "token",
            }

        def json(self):
            return self._data

    def _request(*args, **kwargs):
        return Response()

    requests_stub.post = _request
    requests_stub.get = _request

    sys.modules['requests'] = requests_stub
