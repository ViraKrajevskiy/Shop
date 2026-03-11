# Run server (PowerShell) — можно запускать из корня проекта или из scripts/
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Run .\setup.ps1 first to create venv" -ForegroundColor Red
    exit 1
}
& .\venv\Scripts\Activate.ps1
python manage.py runserver
