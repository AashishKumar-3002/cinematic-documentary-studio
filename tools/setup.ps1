param(
    [switch]$CheckOnly,
    [switch]$WithHtml,
    [switch]$WithResearch
)
$ErrorActionPreference = 'Stop'
$setupRoot = Split-Path $PSScriptRoot -Parent
if ($env:OS -ne 'Windows_NT') { throw 'This bootstrap is tested on Windows. See docs/SETUP.md for manual setup.' }
Push-Location $setupRoot
try {
    . "$PSScriptRoot/env.ps1"
    $setupPython = Join-Path $setupRoot '.venv/Scripts/python.exe'
    if ($CheckOnly) {
        if (-not (Test-Path $setupPython)) { throw 'Missing .venv; run tools/setup.ps1 first.' }
        & $setupPython -c 'import skia,numpy,PIL,scipy,kokoro_onnx,faster_whisper,soundfile'
        if ($LASTEXITCODE -ne 0) { throw 'Core dependency check failed.' }
        Write-Output 'Core Python imports OK'
        & $setupPython tools/download_runtime.py --check
        if ($LASTEXITCODE -ne 0) { throw 'Runtime/model verification failed.' }
        & "$setupRoot/tools/bin/ffmpeg.exe" -version | Select-Object -First 1
        & "$setupRoot/tools/bin/ffprobe.exe" -version | Select-Object -First 1
        return
    }
    if (-not (Test-Path $setupPython)) {
        if (Get-Command py -ErrorAction SilentlyContinue) {
            & py -3.11 -m venv .venv
        } elseif (Get-Command python -ErrorAction SilentlyContinue) {
            & python -m venv .venv
        } else { throw 'Install Python 3.11, then rerun. No system runtime is installed by this script.' }
        if ($LASTEXITCODE -ne 0) { throw 'Could not create .venv; Python 3.11 is recommended.' }
    }
    & $setupPython -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed.' }
    & $setupPython tools/download_runtime.py --models --ffmpeg
    if ($LASTEXITCODE -ne 0) { throw 'Runtime download or verification failed.' }
    if ($WithResearch) {
        & $setupPython -m pip install -r requirements-research.txt
        if ($LASTEXITCODE -ne 0) { throw 'Optional research dependencies failed.' }
        & $setupPython -m playwright install chromium
        if ($LASTEXITCODE -ne 0) { throw 'Optional browser download failed.' }
    }
    if ($WithHtml) {
        if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { throw 'Install Node.js 22.20+ before using -WithHtml.' }
        & npm ci
        if ($LASTEXITCODE -ne 0) { throw 'Optional npm installation failed.' }
    }
    Write-Output 'Setup complete. Load tools/env.ps1 in each new PowerShell session.'
} finally { Pop-Location }
