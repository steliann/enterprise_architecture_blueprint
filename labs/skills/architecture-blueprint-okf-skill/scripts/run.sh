#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ ! -f "$ROOT/.runtime-python" ]]; then
  echo "Skill environment not configured. Run scripts/setup.sh first." >&2
  exit 1
fi
PYTHON_BIN="$(cat "$ROOT/.runtime-python")"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
exec "$PYTHON_BIN" -m architecture_blueprint_okf.cli "$@"
