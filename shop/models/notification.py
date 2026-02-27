from django.conf import settings
from django.db import models


class Notification(models.Model):
    """Уведомление пользователя"""
    TYPE_CHAT = 'chat'
    TYPE_NEW_PRODUCT = 'new_product'

    TYPE_CHOICES = [
        (TYPE_CHAT, 'Сообщение в чате'),
        (TYPE_NEW_PRODUCT, 'Новый товар продавца'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Пользователь'
    )
    ntype = models.CharField('Тип', max_length=20, choices=TYPE_CHOICES)
    title = models.CharField('Заголовок', max_length=200)
    link = models.CharField('Ссылка', max_length=500, blank=True)
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user}: {self.title[:50]}'


class SellerFollow(models.Model):
    """Подписка на продавца"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_sellers',
        verbose_name='Подписчик'
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Продавец'
    )
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка на продавца'
        verbose_name_plural = 'Подписки на продавцов'
        unique_together = [('user', 'seller')]

    def __str__(self):
        return f'{self.user} → {self.seller}'
