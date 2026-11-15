. "$PSScriptRoot/env.ps1"
$env:SKILL_DIR = Join-Path $studioRoot '.agents/skills/last30days'
$researchPython = Join-Path $studioRoot '.research-venv/Scripts/python.exe'
if (!(Test-Path $researchPython)) { throw 'Research runtime missing. See README.md.' }
& $researchPython -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 1)'
if ($LASTEXITCODE -ne 0) { throw 'Last30Days requires Python 3.12+' }
$env:LAST30DAYS_PYTHON = $researchPython
$env:PATH = "$(Split-Path $researchPython -Parent);$env:PATH"
& $researchPython (Join-Path $env:SKILL_DIR 'scripts/last30days.py') @args
exit $LASTEXITCODE
