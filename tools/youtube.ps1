. "$PSScriptRoot/env.ps1"
& "$studioRoot/.venv/Scripts/python.exe" "$studioRoot/tools/youtube_manage.py" @args
exit $LASTEXITCODE
