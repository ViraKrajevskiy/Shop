@echo off
if not exist .env (
    copy .env.example .env
    echo Created .env. Generate SECRET_KEY before production!
)
echo Creating virtual environment...
python -m venv venv

echo Activating and installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Done. To activate: venv\Scripts\activate.bat
echo Then: python manage.py migrate
echo       python manage.py add_sample_data
echo       python manage.py runserver
pause
