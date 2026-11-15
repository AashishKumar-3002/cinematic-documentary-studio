#!/usr/bin/env bash
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh"
exec node "$STUDIO_ROOT/node_modules/hyperframes/bin/hyperframes.mjs" "$@"
