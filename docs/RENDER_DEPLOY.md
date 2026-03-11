# Деплой на Render.com (101-school.uz)

## 1. Подключение репозитория из GitHub

1. Зайдите на [dashboard.render.com](https://dashboard.render.com).
2. **New** → **Web Service**.
3. В разделе **Connect a repository** нажмите **Connect account** для GitHub (если ещё не подключён) и выберите репозиторий с проектом Shop.
4. Подключите репозиторий — Render будет подтягивать код из GitHub при каждом пуше (автодеплой).

## 2. База данных PostgreSQL

1. В Render: **New** → **PostgreSQL** (или в боковом меню **Databases**).
2. Создайте БД (plan Free при необходимости).
3. В карточке БД скопируйте **Internal Database URL** — он понадобится для переменной `DATABASE_URL`.

## 3. Настройки Web Service

| Параметр | Значение |
|----------|----------|
| **Name** | например `shop` или `101-school` |
| **Region** | ближайший к пользователям |
| **Branch** | `main` (или ваша ветка для деплоя) |
| **Root Directory** | оставить пустым |
| **Runtime** | Python 3 |
| **Build Command** | `./build.sh` |
| **Start Command** | `python manage.py migrate --noinput && gunicorn config.wsgi:application` |

> **Release Command** (если есть): `python manage.py migrate --noinput`

## 4. Переменные окружения (Environment)

В Web Service → **Environment** добавьте:

| Key | Value |
|-----|--------|
| `PYTHON_VERSION` | `3.11.0` |
| `SECRET_KEY` | сгенерировать: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `RENDER` | `True` |
| `DATABASE_URL` | Internal Database URL от вашей PostgreSQL (или связать сервис с БД в Render) |
| `ALLOWED_HOSTS_EXTRA` | `101-school.uz,www.101-school.uz` (уже есть по умолчанию в коде, можно не задавать) |
| `CSRF_TRUSTED_ORIGINS` | `https://101-school.uz,https://www.101-school.uz` |
| `SECURE_SSL_REDIRECT` | `True` (рекомендуется при работе по HTTPS) |

Связка с PostgreSQL: в том же разделе Environment можно выбрать **Add Environment Variable** → **Add from Render** и привязать `DATABASE_URL` к созданной БД.

## 5. Кастомный домен 101-school.uz

1. В карточке Web Service откройте **Settings** → **Custom Domains**.
2. **Add Custom Domain** → введите `101-school.uz`.
3. При необходимости добавьте `www.101-school.uz`.
4. Render покажет CNAME-записи (или A-запись). В панели управления доменом (где куплен 101-school.uz) создайте указанные записи.
5. После проверки DNS Render выдаст сертификат SSL — сайт будет открываться по `https://101-school.uz`.

Хосты `101-school.uz` и `www.101-school.uz` уже добавлены в проект через `ALLOWED_HOSTS_EXTRA` и `CSRF_TRUSTED_ORIGINS` по умолчанию.

## 6. Деплой

- После сохранения сервиса Render выполнит первый деплой из GitHub.
- Дальше каждый **push в выбранную ветку** будет запускать новый деплой (если включён Auto-Deploy).

## 7. Суперпользователь

После первого успешного деплоя зайдите на `https://101-school.uz/admin/` (или ваш *.onrender.com URL). Если в проекте есть миграция/команда, создающая суперпользователя (логин/пароль admin) — войдите и смените пароль в разделе аккаунта.

## 8. Медиафайлы

Диск на Render эфемерный — загруженные изображения пропадают при редеплое. Для продакшена лучше настроить внешнее хранилище, например:

- [django-storages](https://django-storages.readthedocs.io/) + S3 или совместимое хранилище
- [Cloudinary](https://cloudinary.com/) для картинок

## 9. Ошибка «no such table»

Если при открытии сайта появляется ошибка про отсутствующие таблицы:

1. Убедитесь, что в **Start Command** есть: `python manage.py migrate --noinput && gunicorn config.wsgi:application`.
2. Выполните **Manual Deploy** в Render (Deploy → Deploy latest commit).

## 10. Blueprint (render.yaml)

В корне проекта есть `render.yaml` — при создании сервиса через **New** → **Blueprint** Render может подхватить репозиторий и часть настроек из этого файла. Домен и часть переменных (например, `CSRF_TRUSTED_ORIGINS`) после создания сервиса лучше проверить и при необходимости добавить вручную в Environment и Custom Domains.
