#!/usr/bin/env bash
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh"
research_python="$STUDIO_ROOT/.research-venv/bin/python"
[ -x "$research_python" ] || { printf '%s\n' 'Run bash tools/setup-research.sh first (Python 3.12+ required).' >&2; exit 1; }
"$research_python" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 1)'
export SKILL_DIR="$STUDIO_ROOT/.agents/skills/last30days"
export LAST30DAYS_PYTHON="$research_python"
export PATH="$STUDIO_ROOT/.research-venv/bin:$PATH"
exec "$research_python" "$SKILL_DIR/scripts/last30days.py" "$@"
