from django.conf import settings
from django.db import models

from .product import Product


class Chat(models.Model):
    """Чат (диалог о товаре)"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        null=True,
        blank=True,
        related_name='chats'
    )
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-created_at']

    def __str__(self):
        return f"Чат #{self.pk}" + (f" ({self.product})" if self.product else "")

    def participants_list(self):
        return list(self.participants.values_list('user', flat=True).distinct())


class ChatParticipant(models.Model):
    """Участник чата"""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats')

    class Meta:
        unique_together = ['chat', 'user']


class Message(models.Model):
    """Сообщение в чате"""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_sent')
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Отправлено', auto_now_add=True)
    edited_at = models.DateTimeField('Изменено', null=True, blank=True)
    is_read = models.BooleanField('Прочитано', default=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.text[:30]}..."
