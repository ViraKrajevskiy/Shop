# Shop — Django магазин

## Первый запуск

1. **Создать .env** (обязательно перед публикацией на GitHub):
```powershell
copy .env.example .env
# Сгенерировать SECRET_KEY и вставить в .env:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

2. Создать виртуальное окружение и установить зависимости:

**PowerShell:**
```powershell
cd D:\Shop
.\setup.ps1
```

**CMD или двойной клик:**
```
setup.bat
```

Или вручную:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1   # PowerShell
# venv\Scripts\activate.bat   # CMD
pip install -r requirements.txt
```

3. Миграции и тестовые данные:

```powershell
.\venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py add_sample_data
python manage.py createsuperuser
```

## Запуск

**PowerShell:**
```powershell
.\run.ps1
```

**CMD:**
```
.\run.bat
```

Или вручную: активировать venv → `python manage.py runserver`

## Безопасность (перед публикацией на GitHub)

- `.env` в .gitignore — секреты не попадут в репозиторий
- SECRET_KEY хранится только в `.env`
- Для продакшена: DEBUG=False, настройте ALLOWED_HOSTS, HTTPS

## collectstatic (для продакшена)

```powershell
python manage.py collectstatic
```

Откройте http://127.0.0.1:8000/

## Структура

- **config/** — настройки Django (settings, urls, wsgi)
- **shop/** — приложение: модели, представления, шаблоны
- **templates/** — HTML-шаблоны с Bootstrap 5

## Верхний бар

- **Логотип** — переход на главную
- **Поиск** — по названию товара и бренда
- **Войти / Выйти** — авторизация
- **Корзина, Избранное** — кнопки (заглушки)

## Главная страница

- **Слева:** список категорий и блок «Новинки и VIP»
- **По центру:** 3 карточки в ряд, вертикальные изображения
- **Карточка:** название бренда сверху, фото, название товара снизу
- **Внизу:** пагинация 1, 2, 3...

## Админка

```
python manage.py createsuperuser
```

Затем: http://127.0.0.1:8000/admin/

## Технологии

HTML, CSS, JavaScript, Bootstrap 5, Django 5
