from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'Магазин'

    def ready(self):
        from django.db.models.signals import post_save
        from django.contrib.auth import get_user_model
        from django.urls import reverse
        from .models import UserProfile, Notification, SellerFollow, Product

        def create_profile(sender, instance, created, **kwargs):
            if created:
                UserProfile.objects.get_or_create(user=instance, defaults={'role': UserProfile.ROLE_USER})

        def notify_followers_new_product(sender, instance, created, **kwargs):
            if created and instance.seller_id:
                for follow in SellerFollow.objects.filter(seller_id=instance.seller_id).select_related('user'):
                    Notification.objects.create(
                        user=follow.user,
                        ntype=Notification.TYPE_NEW_PRODUCT,
                        title=f'Новый товар: {instance.name[:60]}{"..." if len(instance.name) > 60 else ""}',
                        link=reverse('product_detail', args=[instance.pk])
                    )

        post_save.connect(create_profile, sender=get_user_model())
        post_save.connect(notify_followers_new_product, sender=Product)
