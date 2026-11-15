#!/usr/bin/env bash
# Compatible with macOS's Bash 3.2 and newer bash versions on Linux.
set -euo pipefail
setup_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
check_only=0
with_html=0
with_research=0
setup_python=""
usage() {
    printf '%s\n' 'Usage: bash tools/setup.sh [--check-only] [--with-html] [--with-research] [--python /path/to/python3]'
    printf '%s\n' 'From zsh: zsh tools/setup.zsh [the same options]'
    printf '%s\n' 'Requires Python 3.11+, FFmpeg and FFprobe. Installs project-local packages only; never invokes sudo, apt or brew.'
}
while [ "$#" -gt 0 ]; do
    case "$1" in
        --check-only) check_only=1; shift ;;
        --with-html) with_html=1; shift ;;
        --with-research) with_research=1; shift ;;
        --python)
            [ "$#" -ge 2 ] || { printf '%s\n' '--python requires an executable path' >&2; exit 2; }
            setup_python="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) printf 'Unknown option: %s\n' "$1" >&2; usage; exit 2 ;;
    esac
done
case "$(uname -s)" in
    Darwin|Linux) ;;
    *) printf '%s\n' 'Use tools/setup.ps1 on Windows.' >&2; exit 1 ;;
esac
export STUDIO_ROOT="$setup_root"
# shellcheck source=tools/env.sh
source "$setup_root/tools/env.sh"
cd "$setup_root"
venv_python="$setup_root/.venv/bin/python"
if [ "$check_only" -eq 1 ]; then
    [ -x "$venv_python" ] || { printf '%s\n' 'Missing .venv; run setup first.' >&2; exit 1; }
    "$venv_python" -c 'import skia,numpy,PIL,scipy,kokoro_onnx,faster_whisper,soundfile'
    "$venv_python" tools/download_runtime.py --check
    ffmpeg -version | sed -n '1p'
    ffprobe -version | sed -n '1p'
    printf '%s\n' 'Core imports, models and media tools verified.'
    exit 0
fi
if [ ! -x "$venv_python" ]; then
    if [ -z "$setup_python" ]; then
        if command -v python3.11 >/dev/null 2>&1; then setup_python=python3.11
        elif command -v python3 >/dev/null 2>&1; then setup_python=python3
        else printf '%s\n' 'Install Python 3.11 or pass --python /path/to/python3.' >&2; exit 1
        fi
    fi
    "$setup_python" -c 'import sys; assert sys.version_info >= (3,11), "Python 3.11+ required"'
    "$setup_python" -m venv "$setup_root/.venv"
fi
# Fail before downloading models if native system prerequisites are absent.
for tool in ffmpeg ffprobe; do
    command -v "$tool" >/dev/null 2>&1 || {
        printf '%s\n' "$tool is missing. Put a compatible executable in tools/bin or on PATH; see docs/SETUP.md."
        exit 1
    }
done
"$venv_python" -m pip install -r requirements.txt
"$venv_python" tools/download_runtime.py --models --ffmpeg
"$venv_python" -c 'import skia,numpy,PIL,scipy,kokoro_onnx,faster_whisper,soundfile'
if [ "$with_research" -eq 1 ]; then
    "$venv_python" -m pip install -r requirements-research.txt
    "$venv_python" -m playwright install chromium
fi
if [ "$with_html" -eq 1 ]; then
    command -v npm >/dev/null 2>&1 || { printf '%s\n' 'Install Node.js 22.20+ to use --with-html.' >&2; exit 1; }
    node -e 'const v=process.versions.node.split(".").map(Number); if(v[0]<22 || (v[0]===22 && v[1]<20)) process.exit(1)'
    npm ci
fi
printf '%s\n' 'Setup complete.' 'For zsh: source tools/env.zsh' 'For bash: source tools/env.sh'
