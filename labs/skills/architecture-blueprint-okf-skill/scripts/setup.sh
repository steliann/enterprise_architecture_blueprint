#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$(command -v python3 || command -v python)"
if "$PYTHON_BIN" -c 'import yaml, jsonschema, jinja2' >/dev/null 2>&1; then
  printf '%s\n' "$PYTHON_BIN" > "$ROOT/.runtime-python"
  echo "Using existing Python runtime: $PYTHON_BIN"
else
  rm -rf "$ROOT/.venv"
  "$PYTHON_BIN" -m venv "$ROOT/.venv"
  "$ROOT/.venv/bin/python" -m pip install -r "$ROOT/requirements.txt"
  printf '%s\n' "$ROOT/.venv/bin/python" > "$ROOT/.runtime-python"
  echo "Installed dependencies in $ROOT/.venv"
fi
"$(cat "$ROOT/.runtime-python")" -c 'import yaml, jsonschema, jinja2; print("Dependencies available")'
echo "Ready. Run: $ROOT/scripts/run.sh --help"
