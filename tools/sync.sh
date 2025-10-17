#!/usr/bin/env bash
set -euo pipefail

# Load local overrides from .env if present
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

SOLR_URL="${SOLR_URL:-}"
if [ -z "$SOLR_URL" ]; then
  echo "SOLR_URL is not set. Define it in .env or the environment." >&2
  exit 1
fi

echo "Running full Performance History pipeline..."

# Choose Python interpreter, prefer 3.8 if available
PYTHON_BIN="${PYTHON_BIN:-}"
prefer_python() {
  if command -v python3.8 >/dev/null 2>&1; then
    echo "python3.8"
  elif command -v python3 >/dev/null 2>&1; then
    echo "python3"
  else
    echo "python"
  fi
}

# If a venv exists, use it, but ensure it's >= 3.8 if python3.8 is present
if [ -z "${PYTHON_BIN}" ]; then
  if [ -x .venv/bin/python ]; then
    VMAJ=$(.venv/bin/python -c 'import sys; print(sys.version_info[0])' 2>/dev/null || echo 0)
    VMIN=$(.venv/bin/python -c 'import sys; print(sys.version_info[1])' 2>/dev/null || echo 0)
    if [ "$VMAJ" -eq 3 ] && [ "$VMIN" -ge 8 ]; then
      PYTHON_BIN=".venv/bin/python"
    else
      if command -v python3.8 >/dev/null 2>&1; then
        echo "Recreating .venv with Python 3.8..."
        rm -rf .venv
        python3.8 -m venv .venv
        PYTHON_BIN=".venv/bin/python"
      else
        PYTHON_BIN=".venv/bin/python"
      fi
    fi
  else
    PYTHON_BIN="$(prefer_python)"
  fi
fi

# Helper to check requests presence in selected interpreter
check_requests() {
  "$PYTHON_BIN" - <<'PY' >/dev/null 2>&1 || exit 1
import sys
try:
    import requests  # noqa: F401
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
}

if ! check_requests; then
  echo "Python 'requests' not found. Bootstrapping local venv in .venv ..."
  # Create venv if missing
  if [ ! -x .venv/bin/python ]; then
    if command -v python3.8 >/dev/null 2>&1; then
      python3.8 -m venv .venv || {
        echo "Failed to create virtualenv. Install python3.8-venv or create manually." >&2
        exit 1
      }
    elif command -v python3 >/dev/null 2>&1; then
      python3 -m venv .venv || {
        echo "Failed to create virtualenv. Install python3-venv or create manually." >&2
        exit 1
      }
    else
      echo "python3 not found. Please install Python 3.x." >&2
      exit 1
    fi
  fi
  PYTHON_BIN=".venv/bin/python"
  "$PYTHON_BIN" -m pip install -U pip >/dev/null 2>&1 || true
  "$PYTHON_BIN" -m pip install -r requirements.txt
fi

"$PYTHON_BIN" tools/pipeline.py all --solr "$SOLR_URL"

echo "Done."
