"""Создаёт тестовых пользователей для чатов (логин: user1/user2, пароль: test123)."""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Создаёт user1 и user2 для тестирования чатов'

    def handle(self, *args, **options):
        User = get_user_model()
        for username, password in [('user1', 'test123'), ('user2', 'test123')]:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'is_staff': False, 'is_superuser': False}
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Создан: {username} / {password}'))
            else:
                self.stdout.write(f'Уже есть: {username}')
        self.stdout.write(self.style.SUCCESS('Войдите как user1 или user2 для тестирования чатов.'))
