# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_add_user_profile_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcomment',
            name='edited_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Изменён'),
        ),
    ]
