param([string]$PythonPath)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/env.ps1"
$researchExecutable = Join-Path $studioRoot '.research-venv/Scripts/python.exe'
if (-not (Test-Path $researchExecutable)) {
    if ($PythonPath) { & $PythonPath -m venv (Join-Path $studioRoot '.research-venv') }
    else { & py -3.12 -m venv (Join-Path $studioRoot '.research-venv') }
    if ($LASTEXITCODE -ne 0) { throw 'Python 3.12+ is required; use -PythonPath to select it.' }
}
& $researchExecutable -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 1)'
if ($LASTEXITCODE -ne 0) { throw 'The research environment requires Python 3.12+.' }
& $researchExecutable -m pip install -r (Join-Path $studioRoot 'requirements-research-lock.txt')
if ($LASTEXITCODE -ne 0) { throw 'Research dependency installation failed.' }
Write-Output 'Research environment ready. Use tools/last30days.ps1 --help.'
