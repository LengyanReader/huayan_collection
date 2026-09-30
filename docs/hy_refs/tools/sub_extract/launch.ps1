param(
    [Parameter(Mandatory)][string]$Lane,
    [Parameter(Mandatory)][string]$Vids
)
$ErrorActionPreference = "Continue"

# 工具目录（脚本自身所在）
$ToolDir = $PSScriptRoot
# 加载 workspace 路径（从 config.json）
$Conf = Get-Content "$ToolDir\config.json" -Encoding UTF8 | ConvertFrom-Json
$WS = $Conf.workspace
if (-not [System.IO.Path]::IsPathRooted($WS)) { $WS = Join-Path $ToolDir $WS }

# conda env PATH（确保 paddle/torch DLL 可加载）
$env:PATH = "C:\Users\data\miniconda3\envs\hy_py312;C:\Users\data\miniconda3\envs\hy_py312\Library\bin;C:\Users\data\miniconda3\envs\hy_py312\Scripts;" + $env:PATH
$env:LANE = $Lane
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$PY = "C:\Users\data\miniconda3\envs\hy_py312\python.exe"
$vidArr = $Vids -split ','
& $PY "$ToolDir\batch.py" @vidArr *>> "$WS\lane_$Lane.out"
