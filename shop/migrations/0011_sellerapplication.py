# Generated manually
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0010_product_publication_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200, verbose_name='Название компании / магазина')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='Телефон')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий заявителя')),
                ('status', models.CharField(choices=[('pending', 'На рассмотрении'), ('approved', 'Одобрена'), ('rejected', 'Отклонена')], default='pending', max_length=20, verbose_name='Статус')),
                ('reject_reason', models.CharField(blank=True, max_length=500, verbose_name='Причина отказа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата заявки')),
                ('reviewed_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата рассмотрения')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_applications', to=settings.AUTH_USER_MODEL, verbose_name='Рассмотрено')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_applications', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка на продавца',
                'verbose_name_plural': 'Заявки на продавца',
                'ordering': ['-created_at'],
            },
        ),
    ]
