# Данные создаются автоматически при первом деплое (без терминала)
# Логин: admin, пароль: admin123 — смените после входа в /admin/
from django.conf import settings
from django.db import migrations


def create_initial_data(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split('.')
    User = apps.get_model(app_label, model_name)
    Category = apps.get_model('shop', 'Category')
    Brand = apps.get_model('shop', 'Brand')

    # Админ — только если суперпользователей ещё нет
    if not User.objects.filter(is_superuser=True).exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@shop.local',
            password='admin123',
        )
        admin.save()

    # Категории
    for name in ['Футболки', 'Худи', 'Куртки', 'Штаны']:
        Category.objects.get_or_create(name=name)

    # Бренды
    for name in ['URBAN STYLE', 'STREET WEAR', 'PREMIUM']:
        Brand.objects.get_or_create(name=name)


def reverse_empty(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_add_brand_owner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_empty),
    ]
