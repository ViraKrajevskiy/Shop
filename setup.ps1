# Setup for PowerShell
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example. Generate SECRET_KEY and update .env before production!" -ForegroundColor Yellow
}
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
python -m venv venv

Write-Host "Activating and installing dependencies..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

Write-Host "Done." -ForegroundColor Green
Write-Host "To activate: .\venv\Scripts\Activate.ps1"
Write-Host "Then: python manage.py migrate"
Write-Host "      python manage.py add_sample_data"
Write-Host "      python manage.py runserver"
