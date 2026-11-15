. "$PSScriptRoot/env.ps1"
& node "$studioRoot/node_modules/hyperframes/bin/hyperframes.mjs" @args
exit $LASTEXITCODE
