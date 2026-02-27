def favorites_count(request):
    """Количество избранных товаров пользователя"""
    if request.user.is_authenticated:
        from .models import UserFavorite
        return {'favorites_count': UserFavorite.objects.filter(user=request.user).count()}
    return {'favorites_count': 0}


def user_profile(request):
    """Профиль и роль пользователя для шаблонов"""
    if request.user.is_authenticated:
        from .models import UserProfile
        profile = UserProfile.objects.filter(user=request.user).first()
        if not profile:
            profile = UserProfile.objects.create(user=request.user, role=UserProfile.ROLE_USER)
        return {
            'user_profile': profile,
            'is_businessman': profile.is_businessman,
            'is_moderator': profile.is_moderator,
        }
    return {'user_profile': None, 'is_businessman': False, 'is_moderator': False}


def notifications_count(request):
    """Количество непрочитанных уведомлений"""
    if request.user.is_authenticated:
        from .models import Notification
        return {'notifications_count': Notification.objects.filter(user=request.user, is_read=False).count()}
    return {'notifications_count': 0}
