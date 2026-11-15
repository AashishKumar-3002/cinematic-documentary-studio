#!/usr/bin/env bash
set -euo pipefail
research_python=python3.12
if [ "${1:-}" = '--help' ]; then
    printf '%s\n' 'Usage: bash tools/setup-research.sh [--python /path/to/python3.12]' 'Creates .research-venv for Last30Days. No system packages are installed.'
    exit 0
fi
if [ "${1:-}" = '--python' ] && [ "$#" -eq 2 ]; then research_python="$2"
elif [ "$#" -ne 0 ]; then printf '%s\n' 'Use --help for supported arguments.' >&2; exit 2
fi
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh"
if [ ! -x "$STUDIO_ROOT/.research-venv/bin/python" ]; then
    command -v "$research_python" >/dev/null 2>&1 || { printf '%s\n' 'Python 3.12+ is required; pass --python with its executable path.' >&2; exit 1; }
    "$research_python" -c 'import sys; assert sys.version_info >= (3,12), "Python 3.12+ required"'
    "$research_python" -m venv "$STUDIO_ROOT/.research-venv"
fi
"$STUDIO_ROOT/.research-venv/bin/python" -c 'import sys; assert sys.version_info >= (3,12), "Python 3.12+ required"'
"$STUDIO_ROOT/.research-venv/bin/python" -m pip install -r "$STUDIO_ROOT/requirements-research-lock.txt"
printf '%s\n' 'Research environment ready. Use bash tools/last30days.sh --help.'
