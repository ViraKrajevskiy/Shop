from django.conf import settings
from django.db import models


class SellerApplication(models.Model):
    """Заявка на статус продавца"""
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'На рассмотрении'),
        (STATUS_APPROVED, 'Одобрена'),
        (STATUS_REJECTED, 'Отклонена'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seller_applications',
        verbose_name='Пользователь'
    )
    company_name = models.CharField('Название компании / магазина', max_length=200)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    comment = models.TextField('Комментарий заявителя', blank=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    reject_reason = models.CharField('Причина отказа', max_length=500, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications',
        verbose_name='Рассмотрено'
    )
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)
    reviewed_at = models.DateTimeField('Дата рассмотрения', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка на продавца'
        verbose_name_plural = 'Заявки на продавца'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.company_name} ({self.get_status_display()})'
