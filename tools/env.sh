# Source this file in bash, or use env.zsh from zsh. No shell options are changed.
if [ -n "${BASH_VERSION:-}" ]; then
    STUDIO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
elif [ -z "${STUDIO_ROOT:-}" ]; then
    printf '%s\n' 'From zsh use: source tools/env.zsh' >&2
    return 1
fi
export STUDIO_ROOT
export HYPERFRAMES_CACHE_DIR="$STUDIO_ROOT/.cache/hyperframes"
export HYPERFRAMES_CONFIG_DIR="$STUDIO_ROOT/.cache/hyperframes-config"
export HYPERFRAMES_NO_TELEMETRY=1
export HF_HOME="$STUDIO_ROOT/.cache/huggingface"
export HF_HUB_DISABLE_SYMLINKS_WARNING=1
export PLAYWRIGHT_BROWSERS_PATH="$STUDIO_ROOT/.cache/playwright"
export PIP_CACHE_DIR="$STUDIO_ROOT/.cache/pip"
export npm_config_cache="$STUDIO_ROOT/.cache/npm"
export XDG_CACHE_HOME="$STUDIO_ROOT/.cache/xdg"
export LAST30DAYS_CONFIG_DIR="$STUDIO_ROOT/.cache/last30days-config"
export LAST30DAYS_MEMORY_DIR="$STUDIO_ROOT/research/last30days"
export LAST30DAYS_STORE="$STUDIO_ROOT/.cache/last30days/research.sqlite3"
export TMPDIR="$STUDIO_ROOT/.cache/tmp"
mkdir -p "$TMPDIR"
export PATH="$STUDIO_ROOT/tools/bin:$STUDIO_ROOT/.venv/bin:$PATH"
