from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """Профиль пользователя с ролью"""
    ROLE_USER = 'user'
    ROLE_BUSINESSMAN = 'businessman'
    ROLE_MODERATOR = 'moderator'

    ROLE_CHOICES = [
        (ROLE_USER, 'Обычный пользователь'),
        (ROLE_BUSINESSMAN, 'Бизнесмен / Продавец'),
        (ROLE_MODERATOR, 'Модератор'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )
    company_name = models.CharField(
        'Название компании / магазина',
        max_length=200,
        blank=True,
        help_text='Только для бизнесменов'
    )
    phone = models.CharField('Телефон', max_length=30, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'

    @property
    def is_businessman(self):
        return self.role == self.ROLE_BUSINESSMAN

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR
