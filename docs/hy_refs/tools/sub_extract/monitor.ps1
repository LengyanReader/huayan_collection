# monitor.ps1 — 硬字幕提取进度一览
# 扫描 workspace 下所有 vid 子目录，报告各阶段完成状态
$ErrorActionPreference = "SilentlyContinue"
$ToolDir = $PSScriptRoot
$Conf = Get-Content "$ToolDir\config.json" -Encoding UTF8 | ConvertFrom-Json
$WS = $Conf.workspace
if (-not [System.IO.Path]::IsPathRooted($WS)) { $WS = Join-Path $ToolDir $WS }

# 发现所有 vid 目录（含 frames/ 或 ocr_out.tsv 的子目录）
$vidDirs = Get-ChildItem $WS -Directory | Where-Object {
    (Test-Path "$($_.FullName)\frames") -or (Test-Path "$($_.FullName)\runs.tsv")
}
foreach ($vd in $vidDirs) {
    $v = $vd.Name
    $mp4 = if (Test-Path "$WS\$v.mp4") { [int]((Get-Item "$WS\$v.mp4").Length / 1MB) } else { 0 }
    $frames = (Get-ChildItem "$v\frames\frame_*.jpg" -Path $WS).Count
    $reps = (Get-ChildItem "$v\reps\frame_*.jpg" -Path $WS).Count
    $ocr = 0
    $tsv = "$WS\$v\ocr_out.tsv"
    if (Test-Path $tsv) { $ocr = ((Get-Content $tsv).Count - 1) }
    $md = if (Test-Path "$WS\$v\$v.md") { "Y" } else { "-" }
    "{0,-13} mp4={1,5}MB frames={2,6} reps={3,5} ocr={4,5} md={5}" -f $v, $mp4, $frames, $reps, $ocr, $md
}
