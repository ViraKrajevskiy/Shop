# Generated manually
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0008_comment_edited_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ntype', models.CharField(choices=[('chat', 'Сообщение в чате'), ('new_product', 'Новый товар продавца')], max_length=20, verbose_name='Тип')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('link', models.CharField(blank=True, max_length=500, verbose_name='Ссылка')),
                ('is_read', models.BooleanField(default=False, verbose_name='Прочитано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SellerFollow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='Продавец')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_sellers', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписка на продавца',
                'verbose_name_plural': 'Подписки на продавцов',
                'unique_together': {('user', 'seller')},
            },
        ),
    ]
