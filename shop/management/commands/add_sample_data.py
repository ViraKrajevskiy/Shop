"""Добавляет тестовые данные: пользователи с ролями, бренды, категории, товары."""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from shop.models import Brand, Category, Product, UserProfile, SellerApplication

User = get_user_model()


class Command(BaseCommand):
    help = 'Добавляет тестовые данные: админ, модератор, продавцы, пользователи, бренды, категории, товары'

    def handle(self, *args, **options):
        # === Пользователи с ролями ===
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@shop.local', 'is_staff': True, 'is_superuser': True}
        )
        admin_user.set_password('admin123')
        admin_user.save()

        mod_user, _ = User.objects.get_or_create(
            username='moderator',
            defaults={'email': 'mod@shop.local', 'is_staff': True}
        )
        mod_user.set_password('mod123')
        mod_user.save()
        mod_profile, _ = UserProfile.objects.get_or_create(user=mod_user, defaults={'role': UserProfile.ROLE_USER})
        mod_profile.role = UserProfile.ROLE_MODERATOR
        mod_profile.save()
        mod_group, _ = Group.objects.get_or_create(name='Модераторы')
        for model in (Product, SellerApplication):
            ct = ContentType.objects.get_for_model(model)
            for perm in Permission.objects.filter(content_type=ct):
                mod_group.permissions.add(perm)
        mod_user.groups.add(mod_group)

        seller1, _ = User.objects.get_or_create(
            username='seller1',
            defaults={'email': 'seller1@shop.local'}
        )
        seller1.set_password('seller123')
        seller1.save()
        sp1, _ = UserProfile.objects.get_or_create(user=seller1, defaults={'role': UserProfile.ROLE_USER})
        sp1.role = UserProfile.ROLE_BUSINESSMAN
        sp1.company_name = 'Стиль и Мода'
        sp1.save()

        seller2, _ = User.objects.get_or_create(
            username='seller2',
            defaults={'email': 'seller2@shop.local'}
        )
        seller2.set_password('seller123')
        seller2.save()
        sp2, _ = UserProfile.objects.get_or_create(user=seller2, defaults={'role': UserProfile.ROLE_USER})
        sp2.role = UserProfile.ROLE_BUSINESSMAN
        sp2.company_name = 'Urban Wear'
        sp2.save()

        user1, _ = User.objects.get_or_create(
            username='user1',
            defaults={'email': 'user1@shop.local'}
        )
        user1.set_password('user123')
        user1.save()

        # === Бренды и категории ===
        Brand.objects.get_or_create(name='URBAN STYLE', defaults={})
        Brand.objects.get_or_create(name='STREET WEAR', defaults={})
        Brand.objects.get_or_create(name='PREMIUM', defaults={})

        cat1, _ = Category.objects.get_or_create(name='Футболки', defaults={})
        cat2, _ = Category.objects.get_or_create(name='Худи', defaults={})
        cat3, _ = Category.objects.get_or_create(name='Куртки', defaults={})
        cat4, _ = Category.objects.get_or_create(name='Штаны', defaults={})

        brands = list(Brand.objects.all())
        categories = [cat1, cat2, cat3, cat4]
        sellers = [seller1, seller2]

        products = [
            ('Оверсайз футболка чёрная', 'US-TB-001', True, False, 2490, 'Мягкий хлопок, свободный крой. Состав: 100% хлопок.'),
            ('Худи с капюшоном оливковое', 'SW-HD-002', True, True, 4590, 'Утеплённое худи с капюшоном. Состав: хлопок 80%, полиэстер 20%.'),
            ('Куртка-бомбер синяя', 'PM-JB-003', False, True, 5990, 'Классическая куртка-бомбер. Утеплённая подкладка.'),
            ('Карго штаны бежевые', 'US-CG-004', True, False, 3290, 'Удобные карго с боковыми карманами. Прямой крой.'),
            ('Базовый топ белый', 'PM-TP-005', False, True, 1290, 'Минималистичный топ из натурального хлопка.'),
            ('Свитшот серый', 'SW-SW-006', False, False, 2790, 'Тёплый свитшот с начесом. Универсальный серый цвет.'),
            ('Парка с мехом', 'PM-PK-007', True, True, 8990, 'Зимняя парка с искусственным мехом в капюшоне.'),
            ('Джинсы зауженные', 'SW-JN-008', False, False, 3490, 'Джинсы слим-фит. Стрейч для комфорта.'),
            ('Лонгслив чёрный', 'US-LS-009', True, False, 1990, 'Базовый лонгслив. Хлопок премиум качества.'),
        ]

        for i, (name, model, vip, new, price, desc) in enumerate(products):
            Product.objects.update_or_create(
                name=name,
                defaults={
                    'model': model,
                    'brand': brands[i % len(brands)],
                    'category': categories[i % len(categories)],
                    'seller': sellers[i % len(sellers)],
                    'is_vip': vip,
                    'is_new': new,
                    'price': price,
                    'description': desc,
                    'publication_status': Product.STATUS_APPROVED,
                }
            )

        # === Заявки на продавца (для проверки модерации) ===
        if not SellerApplication.objects.filter(user=user1).exists():
            SellerApplication.objects.create(
                user=user1,
                company_name='ООО "Тестовый магазин"',
                phone='+7 999 111-22-33',
                comment='Хочу продавать одежду на площадке.',
                status=SellerApplication.STATUS_PENDING
            )
        user2, _ = User.objects.get_or_create(username='user2', defaults={'email': 'user2@shop.local'})
        user2.set_password('user123')
        user2.save()
        UserProfile.objects.get_or_create(user=user2, defaults={'role': UserProfile.ROLE_USER})
        if not SellerApplication.objects.filter(user=user2).exists():
            SellerApplication.objects.create(
                user=user2,
                company_name='Бренд Street Style',
                phone='+7 999 444-55-66',
                comment='Магазин уличной одежды.',
                status=SellerApplication.STATUS_PENDING
            )

        # === Товар на модерации (для проверки) ===
        Product.objects.update_or_create(
            name='Тестовый товар на модерации',
            defaults={
                'model': 'TEST-001',
                'brand': brands[0],
                'category': cat1,
                'seller': seller1,
                'is_vip': False,
                'is_new': False,
                'price': 1500,
                'description': 'Товар в статусе «На модерации» — проверьте в админке.',
                'publication_status': Product.STATUS_PENDING,
            }
        )

        self.stdout.write(self.style.SUCCESS('Тестовые данные добавлены.'))
        self.stdout.write('')
        self.stdout.write('Логины для входа:')
        self.stdout.write('  Admin (всё):     admin / admin123')
        self.stdout.write('  Модератор:       moderator / mod123')
        self.stdout.write('  Продавец 1:      seller1 / seller123  (Стиль и Мода)')
        self.stdout.write('  Продавец 2:      seller2 / seller123  (Urban Wear)')
        self.stdout.write('  Пользователь:    user1 / user123  (есть заявка на рассмотрении)')
        self.stdout.write('  Пользователь:    user2 / user123  (есть заявка на рассмотрении)')
        self.stdout.write('')
        self.stdout.write('Для проверки:')
        self.stdout.write('  - Заявки user1, user2: /admin/ -> Заявки на продавца')
        self.stdout.write('  - Товар "Тестовый товар на модерации": /admin/ -> Товары')
