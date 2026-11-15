$nyosRoot = Split-Path -Parent $PSScriptRoot
$nyosProject = Join-Path $nyosRoot 'projects/lake-nyos/film'
$nyosCheckpointStatus = Join-Path $nyosProject 'out/render-progress.json'
if (Test-Path -LiteralPath $nyosCheckpointStatus) {
    $nyosProgress = Get-Content -Raw $nyosCheckpointStatus | ConvertFrom-Json
    $nyosRunning = $null -ne (Get-Process -Id $nyosProgress.pid -ErrorAction SilentlyContinue)
    $nyosProgress | Add-Member -NotePropertyName process_running -NotePropertyValue $nyosRunning -Force
    if (-not $nyosRunning -and $nyosProgress.state -notlike 'complete*') {
        $nyosProgress.state = 'interrupted; saved sections can be resumed'
    }
    $nyosProgress | ConvertTo-Json
    return
}
$nyosTiming = Get-Content -Raw (Join-Path $nyosProject 'audio/timing.json') | ConvertFrom-Json
$nyosTotalFrames = [int][math]::Round($nyosTiming.total_duration * 30)
$nyosBytesPerFrame = 1920 * 1080 * 3
$nyosEncoders = @(Get-CimInstance Win32_Process -Filter "Name='ffmpeg.exe'" | Where-Object {
    $_.CommandLine -like '*lake-nyos*film*out*chunks*c*.mp4*' -and $_.CommandLine -like '*1920x1080*'
})
$nyosConsumedFrames = 0
foreach ($nyosEncoder in $nyosEncoders) {
    $nyosConsumedFrames += [math]::Floor([double]$nyosEncoder.ReadTransferCount / $nyosBytesPerFrame)
}
# Closed chunks have final MP4 metadata; active chunks are deliberately not probed.
foreach ($nyosChunk in Get-ChildItem (Join-Path $nyosProject 'out/chunks') -Filter 'c*.mp4') {
    if ($nyosChunk.Length -gt 0 -and -not ($nyosEncoders | Where-Object { $_.CommandLine.Contains($nyosChunk.FullName) })) {
        $nyosCount = & (Join-Path $nyosRoot 'tools/bin/ffprobe.exe') -v error -select_streams v:0 -show_entries stream=nb_frames -of csv=p=0 $nyosChunk.FullName
        if ($LASTEXITCODE -eq 0 -and $nyosCount -match '^\d+$') { $nyosConsumedFrames += [int]$nyosCount }
    }
}
[pscustomobject]@{
    approximate_frames = $nyosConsumedFrames
    total_frames = $nyosTotalFrames
    approximate_percent = [math]::Round(100 * $nyosConsumedFrames / $nyosTotalFrames, 1)
    active_encoders = $nyosEncoders.Count
    observed_at = (Get-Date -Format 'HH:mm:ss')
} | ConvertTo-Json
