#!/usr/bin/env zsh
# zsh entry point; use the shared bash implementation on both macOS and Linux.
set -eu
setup_dir="${0:A:h}"
exec bash "$setup_dir/setup.sh" "$@"
