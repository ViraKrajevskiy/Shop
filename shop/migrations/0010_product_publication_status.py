# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_notifications_sellerfollow'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='publication_status',
            field=models.CharField(
                choices=[('pending', 'На модерации'), ('approved', 'Одобрено'), ('rejected', 'Отклонено')],
                default='approved',
                max_length=20,
                verbose_name='Статус публикации'
            ),
        ),
    ]
