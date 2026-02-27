from django.contrib import admin
from django.utils import timezone
from .models import Brand, Category, Product, ProductLike, ProductComment, UserFavorite, Chat, Message, ChatParticipant, UserProfile, SellerApplication


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'brand', 'category', 'seller', 'publication_status', 'price', 'is_vip', 'is_new', 'created_at']
    list_filter = ['brand', 'category', 'publication_status', 'is_vip', 'is_new']
    search_fields = ['name', 'model', 'brand__name', 'description']
    list_editable = ['publication_status']
    actions = ['approve_products', 'reject_products']

    @admin.action(description='Одобрить публикацию')
    def approve_products(self, request, queryset):
        from .models import Product
        updated = queryset.update(publication_status=Product.STATUS_APPROVED)
        self.message_user(request, f'Одобрено товаров: {updated}')

    @admin.action(description='Отклонить публикацию')
    def reject_products(self, request, queryset):
        from .models import Product
        updated = queryset.update(publication_status=Product.STATUS_REJECTED)
        self.message_user(request, f'Отклонено товаров: {updated}')


@admin.register(SellerApplication)
class SellerApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'phone', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username', 'company_name']
    raw_id_fields = ['user', 'reviewed_by']
    readonly_fields = ['created_at']
    actions = ['approve_applications', 'reject_applications']

    @admin.action(description='Одобрить заявки')
    def approve_applications(self, request, queryset):
        pending = queryset.filter(status=SellerApplication.STATUS_PENDING)
        for app in pending:
            app.status = SellerApplication.STATUS_APPROVED
            app.reviewed_by = request.user
            app.reviewed_at = timezone.now()
            app.save()
            profile, _ = UserProfile.objects.get_or_create(user=app.user, defaults={'role': UserProfile.ROLE_USER})
            profile.role = UserProfile.ROLE_BUSINESSMAN
            profile.company_name = app.company_name
            profile.phone = app.phone
            profile.save()
        usernames = ', '.join(a.user.username for a in pending)
        self.message_user(request, f'Одобрено заявок: {pending.count()}. Логины: {usernames} — пусть войдут под своим паролем.')

    @admin.action(description='Отклонить заявки')
    def reject_applications(self, request, queryset):
        pending = queryset.filter(status=SellerApplication.STATUS_PENDING)
        for app in pending:
            app.status = SellerApplication.STATUS_REJECTED
            app.reviewed_by = request.user
            app.reviewed_at = timezone.now()
            app.save()
        self.message_user(request, f'Отклонено заявок: {pending.count()}')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'company_name', 'created_at']
    list_filter = ['role']
    search_fields = ['user__username', 'company_name']
    raw_id_fields = ['user']


@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'text_short', 'created_at']

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Текст'


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'created_at']
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender', 'text_short', 'created_at', 'is_read']

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Текст'
