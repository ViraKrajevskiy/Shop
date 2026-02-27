from django.conf import settings
from django.db import models

from .brand import Brand
from .category import Category


class Product(models.Model):
    """Товар"""
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'На модерации'),
        (STATUS_APPROVED, 'Одобрено'),
        (STATUS_REJECTED, 'Отклонено'),
    ]

    name = models.CharField('Название', max_length=200)
    model = models.CharField('Модель / артикул', max_length=80, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Продавец',
        related_name='products_for_sale'
    )
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, null=True, blank=True)
    is_vip = models.BooleanField('VIP товар', default=False)
    is_new = models.BooleanField('Новинка', default=False)
    publication_status = models.CharField(
        'Статус публикации',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_APPROVED
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductLike(models.Model):
    """Лайк товара"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='product_likes'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='likes'
    )
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = [('user', 'product')]

    def __str__(self):
        return f'{self.user} → {self.product}'


class ProductComment(models.Model):
    """Комментарий к товару"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='product_comments'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='comments'
    )
    text = models.TextField('Текст', max_length=1000)
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    edited_at = models.DateTimeField('Изменён', null=True, blank=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user}: {self.text[:30]}...'


class UserFavorite(models.Model):
    """Избранное пользователя (товар в избранном)"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_favorites'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='favorites'
    )
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = [('user', 'product')]

    def __str__(self):
        return f'{self.user} ↔ {self.product}'
