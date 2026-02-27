# Run server (PowerShell)
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Run .\setup.ps1 first to create venv" -ForegroundColor Red
    exit 1
}
& .\venv\Scripts\Activate.ps1
python manage.py runserver
