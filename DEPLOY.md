# Деплой на свой сервер (VPS)

Инструкция для запуска проекта на своём сервере (VPS, VDS) с доменом 101-school.uz. Без Render и прочих PaaS.

## 1. Сервер

- Сервер с Ubuntu/Debian (или другим Linux).
- Домен 101-school.uz направлен на IP сервера (A-запись или CNAME).

## 2. Установка на сервере

```bash
# Обновление и базовые пакеты
sudo apt update && sudo apt install -y python3.11 python3.11-venv python3-pip nginx

# Клонирование из GitHub
cd /var/www
sudo git clone https://github.com/ВАШ_ЛОГИН/ВАШ_РЕПОЗИТОРИЙ.git shop
cd shop
```

Дальше подтягивать обновления: `git pull`.

## 3. Окружение и зависимости

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

## 4. Переменные окружения

Создайте файл `.env` в корне проекта (или задайте переменные в systemd):

```env
SECRET_KEY=ваш-сгенерированный-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=101-school.uz,www.101-school.uz,localhost,127.0.0.1
DATABASE_URL=postgres://user:password@localhost:5432/shop_db
CSRF_TRUSTED_ORIGINS=https://101-school.uz,https://www.101-school.uz
SECURE_SSL_REDIRECT=True
```

Сгенерировать `SECRET_KEY`:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Для SQLite вместо PostgreSQL просто не задавайте `DATABASE_URL` — в проекте будет использоваться SQLite (для продакшена лучше PostgreSQL).

## 5. База данных и миграции

**PostgreSQL:**
```bash
sudo -u postgres createdb shop_db
sudo -u postgres createuser -P shop_user  # задать пароль
# В .env: DATABASE_URL=postgres://shop_user:пароль@localhost:5432/shop_db
```

**Миграции и статика:**
```bash
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 6. Gunicorn

Проверка запуска:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

Для постоянной работы — systemd. Файл `/etc/systemd/system/shop.service`:

```ini
[Unit]
Description=Shop Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/shop
Environment="PATH=/var/www/shop/venv/bin"
ExecStart=/var/www/shop/venv/bin/gunicorn config.wsgi:application --bind unix:/var/www/shop/sock/gunicorn.sock --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo mkdir -p /var/www/shop/sock
sudo chown www-data:www-data /var/www/shop/sock
sudo systemctl daemon-reload
sudo systemctl enable shop
sudo systemctl start shop
```

## 7. Nginx

Файл `/etc/nginx/sites-available/shop`:

```nginx
server {
    listen 80;
    server_name 101-school.uz www.101-school.uz;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name 101-school.uz www.101-school.uz;

    ssl_certificate     /etc/letsencrypt/live/101-school.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/101-school.uz/privkey.pem;

    root /var/www/shop;
    client_max_body_size 20M;

    location /static/ {
        alias /var/www/shop/staticfiles/;
    }
    location /media/ {
        alias /var/www/shop/media/;
    }
    location / {
        proxy_pass http://unix:/var/www/shop/sock/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Включить сайт и перезапустить nginx:
```bash
sudo ln -s /etc/nginx/sites-available/shop /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

## 8. SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d 101-school.uz -d www.101-school.uz
```

## 9. Обновление с GitHub

```bash
cd /var/www/shop
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart shop
```

---

**Медиафайлы:** на VPS они хранятся в `/var/www/shop/media/`. Для резервного копирования добавьте эту папку в бэкапы. Для больших объёмов можно позже настроить S3 или другой объектный сторедж.
