#!/usr/bin/env bash
set -euo pipefail

# Load local overrides from .env if present
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

SOLR_URL="${SOLR_URL:-http://192.168.198.156:9993/solr/assets/select}"

echo "Running full Performance History pipeline..."

# Check for requests>=2.31.0; avoid installing unless necessary
REQ_CHECK=$(python3 - <<'PY'
min=(2,31,0)
def parse(v):
    try:
        parts=[int(x) for x in v.split('.')[:3]]
        while len(parts)<3:
            parts.append(0)
        return tuple(parts)
    except Exception:
        return (0,0,0)
try:
    import requests
    print('OK' if parse(requests.__version__) >= min else 'MISSING')
except Exception:
    print('MISSING')
PY
)

if [ "$REQ_CHECK" != "OK" ]; then
  echo "Missing Python dependency: requests>=2.31.0"
  echo "Create a virtualenv and install requirements, e.g.:"
  echo "  python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

python3 tools/pipeline.py all --solr "$SOLR_URL"

echo "Done."
