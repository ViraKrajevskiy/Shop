"""
URL configuration for Shop project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.home, name='home_by_category'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/category/<int:category_id>/', views.catalog, name='catalog_by_category'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/like/', views.like_toggle, name='like_toggle'),
    path('product/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('product/comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('product/comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('favorites/add/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:pk>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('create/', views.create_listing, name='create_listing'),
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/products/', views.seller_products, name='seller_products'),
    path('seller/brand/', views.seller_brand, name='seller_brand'),
    path('chats/', views.chat_list, name='chat_list'),
    path('chats/<int:pk>/', views.chat_detail, name='chat_detail'),
    path('chats/message/<int:pk>/edit/', views.message_edit, name='message_edit'),
    path('chats/message/<int:pk>/delete/', views.message_delete, name='message_delete'),
    path('chats/start/', views.chat_start, name='chat_start'),
    path('product/<int:pk>/chat/', views.chat_start_product, name='chat_start_product'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('become-seller/', views.become_seller, name='become_seller'),
    path('profile/', views.profile_view, name='profile'),
    path('support/', views.support_view, name='support'),
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<int:pk>/read/', views.notification_read, name='notification_read'),
    path('seller/<int:pk>/follow/', views.follow_seller, name='follow_seller'),
    path('seller/<int:pk>/unfollow/', views.unfollow_seller, name='unfollow_seller'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
