from django.conf import settings
from django.db import models


class Brand(models.Model):
    """Бренд товара (производитель или собственный бренд продавца)"""
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'На подтверждении'),
        (STATUS_APPROVED, 'Подтверждён'),
    ]
    name = models.CharField('Название', max_length=100)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_APPROVED,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Владелец (продавец)',
        related_name='owned_brands'
    )

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name
