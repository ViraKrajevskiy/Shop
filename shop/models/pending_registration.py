from django.db import models


class PendingRegistration(models.Model):
    """Ожидающая подтверждения регистрация по коду из email."""
    email = models.EmailField('Email')
    username = models.CharField('Логин', max_length=150)
    password = models.CharField('Пароль (hash)', max_length=128)  # хэш для User.password
    code = models.CharField('Код подтверждения', max_length=10)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Ожидающая регистрация'
        verbose_name_plural = 'Ожидающие регистрации'

    def __str__(self):
        return f'{self.email} ({self.username})'
