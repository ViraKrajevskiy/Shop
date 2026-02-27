# Деплой на Render.com

## Быстрый старт

1. **Репозиторий**: Залейте проект в GitHub/GitLab и подключите к Render.
2. **PostgreSQL**: В Render Dashboard → Databases → Create PostgreSQL. Скопируйте Internal Database URL.
3. **Web Service**: New → Web Service, выберите репозиторий.

## Настройки Web Service

| Параметр | Значение |
|----------|----------|
| **Build Command** | `./build.sh` |
| **Release Command** | `python manage.py migrate --noinput` |
| **Start Command** | `gunicorn config.wsgi:application` |
| **Runtime** | Python 3 |

> ⚠️ **Build Command** обязательно `./build.sh` — иначе не выполняются collectstatic и migrate.

## Переменные окружения (Environment Variables)

| Переменная | Обязательно | Описание |
|------------|-------------|----------|
| `SECRET_KEY` | Да | Сгенерировать: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | Да | `False` |
| `DATABASE_URL` | Да | Internal Database URL от PostgreSQL (Render подставит автоматически при связке) |
| `RENDER` | Да | `True` (Render сам добавит хост в ALLOWED_HOSTS) |
| `ALLOWED_HOSTS` | Опционально | `your-app.onrender.com` (или домен) |
| `SECURE_SSL_REDIRECT` | Опционально | `True` |
| `CSRF_TRUSTED_ORIGINS` | Опционально | `https://your-app.onrender.com` |

## Связка с PostgreSQL

1. В Web Service → Environment → Add Environment Variable
2. Key: `DATABASE_URL`
3. Value: выберите из Related Services → ваш PostgreSQL → Internal Database URL

Либо в Render Dashboard свяжите Web Service с PostgreSQL — переменная подтянется автоматически.

## Суперпользователь

После деплоя: Dashboard → Shell → выполнить:

```
python manage.py createsuperuser
```

## Ошибка `no such table: shop_product`

В Render Dashboard → ваш сервис shop → **Settings**:

1. **Build Command** → замените на `./build.sh` (если там `pip install -r requirements.txt`, миграции не выполняются).
2. **Release Command** → добавьте `python manage.py migrate --noinput` (если нет).
3. **PostgreSQL**: Создайте БД, добавьте `DATABASE_URL`. Без неё используется SQLite — диск эфемерный, данные теряются при редеплое.

Затем **Manual Deploy** → Deploy latest commit.

## Outbound IP (для whitelist)

Запросы к внешним API идут с IP Render. Для настройки whitelist в платёжных системах, базах и т.п.:

| Диапазон | CIDR |
|----------|------|
| 74.220.48.0/24 | 74.220.48.0–74.220.48.255 |
| 74.220.56.0/24 | 74.220.56.0–74.220.56.255 |

> Сервис: https://shop-v82z.onrender.com/

## Медиафайлы

Диск на Render **эфемерный** — загруженные изображения товаров теряются при каждом редеплое.

Для продакшена рекомендуется:
- [AWS S3](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html) + django-storages
- [Cloudinary](https://cloudinary.com/) для изображений
