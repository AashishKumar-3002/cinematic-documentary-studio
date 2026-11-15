#!/usr/bin/env bash
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh"
exec "$STUDIO_ROOT/.venv/bin/python" "$STUDIO_ROOT/.agents/skills/learn/scripts/fetch.py" "$@"
