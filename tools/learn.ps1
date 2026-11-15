. "$PSScriptRoot/env.ps1"
& "$studioRoot/.venv/Scripts/python.exe" "$studioRoot/.agents/skills/learn/scripts/fetch.py" @args
exit $LASTEXITCODE
