@echo off
if not exist venv\Scripts\activate.bat (
    echo Run setup.bat first to create venv
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
python manage.py runserver
pause
