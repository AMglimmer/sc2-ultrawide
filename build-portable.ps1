param([ValidateSet('onefile', 'onedir')][string]$Mode = 'onefile')
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    $python = Join-Path $PSScriptRoot '.venv-build\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $python)) { throw 'Create .venv-build and install requirements-build.txt first.' }
    & $python -m PyInstaller --noconfirm --clean "--$Mode" --windowed --noupx --name SC2-Ultrawide-Portable --distpath "dist\$Mode" --workpath "build\$Mode" --specpath build sc2_ultrawide_gui.py
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller build failed.' }
} finally { Pop-Location }
