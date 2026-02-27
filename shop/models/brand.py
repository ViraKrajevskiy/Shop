from django.conf import settings
from django.db import models


class Brand(models.Model):
    """Бренд товара (производитель или собственный бренд продавца)"""
    name = models.CharField('Название', max_length=100)
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
