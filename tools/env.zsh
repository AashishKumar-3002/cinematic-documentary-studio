# Source from zsh to keep caches and the virtual environment inside this checkout.
typeset -g STUDIO_ROOT="${${(%):-%x}:A:h:h}"
source "$STUDIO_ROOT/tools/env.sh"
