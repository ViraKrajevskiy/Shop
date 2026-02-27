from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, logout
from .models import Product, Category, Brand, Chat, ChatParticipant, Message, ProductLike, ProductComment, UserFavorite, UserProfile, Notification, SellerFollow, SellerApplication
from decimal import Decimal


def home(request, category_id=None):
    """Главная страница. Продавцы перенаправляются в кабинет."""
    profile = getattr(request.user, 'profile', None) if request.user.is_authenticated else None
    if profile and profile.is_businessman:
        return redirect('seller_dashboard')
    return _catalog_view(request, category_id)


def catalog(request, category_id=None):
    """Каталог товаров (для продавцов — без редиректа)"""
    return _catalog_view(request, category_id)


def _catalog_view(request, category_id=None):
    """Общая логика каталога"""
    categories = Category.objects.filter(
        pk__in=Product.objects.filter(publication_status=Product.STATUS_APPROVED).values_list('category_id', flat=True).distinct()
    ).order_by('name')
    brands = Brand.objects.filter(
        pk__in=Product.objects.filter(publication_status=Product.STATUS_APPROVED).values_list('brand_id', flat=True).distinct()
    ).order_by('name')
    vip_and_new = Product.objects.filter(
        publication_status=Product.STATUS_APPROVED
    ).filter(
        Q(is_vip=True) | Q(is_new=True)
    ).distinct()[:6]

    products = Product.objects.filter(publication_status=Product.STATUS_APPROVED).select_related(
        'brand', 'category', 'seller', 'seller__profile'
    ).annotate(
        likes_count=Count('likes'),
        comments_count=Count('comments')
    )

    if category_id:
        products = products.filter(category_id=category_id)

    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )

    brand_id_raw = request.GET.get('brand')
    brand_id = int(brand_id_raw) if brand_id_raw and brand_id_raw.isdigit() else None
    if brand_id:
        products = products.filter(brand_id=brand_id)

    try:
        price_min = request.GET.get('price_min')
        if price_min and price_min.strip():
            products = products.filter(price__gte=Decimal(price_min.strip()))
    except (ValueError, TypeError):
        pass
    try:
        price_max = request.GET.get('price_max')
        if price_max and price_max.strip():
            products = products.filter(price__lte=Decimal(price_max.strip()))
    except (ValueError, TypeError):
        pass

    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    liked_ids = set()
    favorites_ids = set()
    followed_seller_ids = set()
    if request.user.is_authenticated and page_obj:
        product_ids = [p.id for p in page_obj]
        liked_ids = set(ProductLike.objects.filter(
            user=request.user,
            product_id__in=product_ids
        ).values_list('product_id', flat=True))
        favorites_ids = set(UserFavorite.objects.filter(
            user=request.user,
            product_id__in=product_ids
        ).values_list('product_id', flat=True))
        seller_ids = [p.seller_id for p in page_obj if p.seller_id]
        if seller_ids:
            followed_seller_ids = set(SellerFollow.objects.filter(
                user=request.user,
                seller_id__in=seller_ids
            ).values_list('seller_id', flat=True))

    return render(request, 'shop/home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'vip_and_new': vip_and_new,
        'current_category_id': category_id,
        'search_query': search_query,
        'current_brand_id': brand_id,
        'price_min': request.GET.get('price_min', ''),
        'price_max': request.GET.get('price_max', ''),
        'current_sort': sort,
        'liked_ids': liked_ids,
        'favorites_ids': favorites_ids,
        'followed_seller_ids': followed_seller_ids,
        'catalog_mode': request.resolver_match.url_name.startswith('catalog'),
    })


def product_detail(request, pk):
    """Страница товара с описанием"""
    product = get_object_or_404(
        Product.objects.select_related('brand', 'category', 'seller', 'seller__profile').annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments')
        ),
        pk=pk
    )
    profile = getattr(request.user, 'profile', None) if request.user.is_authenticated else None
    can_view = (
        product.publication_status == Product.STATUS_APPROVED or
        (profile and profile.is_moderator) or
        (request.user.is_authenticated and product.seller_id == request.user.id)
    )
    if not can_view:
        from django.http import Http404
        raise Http404('Товар недоступен')
    is_in_favorites = (
        request.user.is_authenticated and
        UserFavorite.objects.filter(user=request.user, product=product).exists()
    )
    is_liked = request.user.is_authenticated and ProductLike.objects.filter(
        user=request.user, product=product
    ).exists()
    is_following_seller = (
        request.user.is_authenticated and product.seller_id and
        SellerFollow.objects.filter(user=request.user, seller_id=product.seller_id).exists()
    )
    comments = product.comments.select_related('user').order_by('-created_at')[:20]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'is_in_favorites': is_in_favorites,
        'is_liked': is_liked,
        'is_following_seller': is_following_seller,
        'comments': comments,
    })


@login_required
def add_to_favorites(request, pk):
    """Добавить товар в избранное (только для авторизованных)"""
    product = get_object_or_404(Product, pk=pk)
    UserFavorite.objects.get_or_create(user=request.user, product=product)
    count = UserFavorite.objects.filter(user=request.user).count()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'action': 'add', 'count': count})
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)


@login_required
def remove_from_favorites(request, pk):
    """Убрать из избранного (только для авторизованных)"""
    UserFavorite.objects.filter(user=request.user, product_id=pk).delete()
    count = UserFavorite.objects.filter(user=request.user).count()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'action': 'remove', 'count': count})
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)


@login_required
def like_toggle(request, pk):
    """Переключить лайк товара (AJAX)"""
    product = get_object_or_404(Product, pk=pk)
    like, created = ProductLike.objects.get_or_create(user=request.user, product=product)
    if not created:
        like.delete()
        count = ProductLike.objects.filter(product=product).count()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'action': 'remove', 'count': count})
        return redirect(request.GET.get('next', request.META.get('HTTP_REFERER', '/')))
    count = ProductLike.objects.filter(product=product).count()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'action': 'add', 'count': count})
    return redirect(request.GET.get('next', request.META.get('HTTP_REFERER', '/')))


@login_required
def add_comment(request, pk):
    """Добавить комментарий к товару"""
    product = get_object_or_404(Product, pk=pk)
    text = (request.POST.get('text') or '').strip()[:1000]
    if text:
        ProductComment.objects.create(user=request.user, product=product, text=text)
    return redirect('product_detail', pk=pk)


@login_required
def comment_edit(request, pk):
    """Редактировать свой комментарий"""
    from django.utils import timezone
    comment = get_object_or_404(ProductComment.objects.select_related('product'), pk=pk)
    if comment.user_id != request.user.id:
        return redirect('product_detail', pk=comment.product_id)
    text = (request.POST.get('text') or '').strip()[:1000]
    if text:
        comment.text = text
        comment.edited_at = timezone.now()
        comment.save()
    return redirect('product_detail', pk=comment.product_id)


@login_required
def comment_delete(request, pk):
    """Удалить свой комментарий"""
    comment = get_object_or_404(ProductComment.objects.select_related('product'), pk=pk)
    if comment.user_id != request.user.id:
        return redirect('product_detail', pk=comment.product_id)
    product_id = comment.product_id
    comment.delete()
    return redirect('product_detail', pk=product_id)


@login_required
def favorites_list(request):
    """Страница избранного (только для авторизованных)"""
    favorites = list(UserFavorite.objects.filter(user=request.user).values_list('product_id', flat=True))
    products = Product.objects.filter(pk__in=favorites).annotate(
        likes_count=Count('likes'),
        comments_count=Count('comments')
    ).select_related('brand', 'category') if favorites else []
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    liked_ids = set()
    if request.user.is_authenticated and page_obj:
        liked_ids = set(ProductLike.objects.filter(
            user=request.user,
            product_id__in=[p.id for p in page_obj]
        ).values_list('product_id', flat=True))
    return render(request, 'shop/favorites.html', {
        'page_obj': page_obj,
        'favorites_ids': favorites,
        'liked_ids': liked_ids,
    })


@login_required
def become_seller(request):
    """Заявка на статус продавца — отправляется на модерацию"""
    profile = getattr(request.user, 'profile', None)
    if profile and profile.is_businessman:
        messages.info(request, 'Вы уже зарегистрированы как продавец.')
        return redirect('create_listing')
    pending = SellerApplication.objects.filter(user=request.user, status=SellerApplication.STATUS_PENDING).first()
    if pending:
        return render(request, 'shop/become_seller.html', {'form': None, 'pending_application': pending})
    if request.method == 'POST':
        from .forms import BecomeSellerForm
        form = BecomeSellerForm(request.POST)
        if form.is_valid():
            SellerApplication.objects.create(
                user=request.user,
                company_name=form.cleaned_data['company_name'].strip(),
                phone=(form.cleaned_data.get('phone') or '').strip(),
                comment=(form.cleaned_data.get('comment') or '').strip()
            )
            messages.success(request, 'Заявка отправлена! Модерация рассмотрит её в ближайшее время.')
            return redirect('home')
    else:
        from .forms import BecomeSellerForm
        form = BecomeSellerForm()
    return render(request, 'shop/become_seller.html', {'form': form})


def register_view(request):
    """Регистрация: обычный пользователь или продавец (бизнесмен)"""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        from .forms import RegisterForm
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            next_url = request.GET.get('next') or request.POST.get('next') or '/'
            return redirect(next_url)
    else:
        from .forms import RegisterForm
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})


@login_required
def create_listing(request):
    """Подать объявление — только для продавцов (бизнесменов)"""
    profile = getattr(request.user, 'profile', None)
    if not profile or not profile.is_businessman:
        messages.warning(request, 'Размещать товары могут только продавцы. Заполните заявку на статус продавца.')
        return redirect('become_seller')

    from .forms import ProductForm

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.publication_status = Product.STATUS_PENDING

            resolved = form.cleaned_data.get('_resolved_brand')
            brand_new = form.cleaned_data.get('_brand_to_create')
            if resolved:
                product.brand = resolved
            elif brand_new:
                product.brand = Brand.objects.create(name=brand_new, owner=request.user)

            product.save()
            messages.success(request, 'Объявление размещено! Оно появится в каталоге после модерации.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(user=request.user)

    has_owned_brands = Brand.objects.filter(owner=request.user).exists()
    return render(request, 'shop/create_listing.html', {'form': form, 'has_owned_brands': has_owned_brands})


@login_required
def seller_dashboard(request):
    """Личный кабинет продавца — статистика и управление"""
    profile = getattr(request.user, 'profile', None)
    if not profile or not profile.is_businessman:
        messages.warning(request, 'Доступно только для продавцов.')
        return redirect('become_seller')
    products = Product.objects.filter(seller=request.user)
    stats = {
        'total': products.count(),
        'approved': products.filter(publication_status=Product.STATUS_APPROVED).count(),
        'pending': products.filter(publication_status=Product.STATUS_PENDING).count(),
        'rejected': products.filter(publication_status=Product.STATUS_REJECTED).count(),
    }
    products_annotated = products.annotate(
        likes_count=Count('likes'),
        comments_count=Count('comments'),
        favorites_count=Count('favorites')
    ).select_related('brand', 'category').order_by('-created_at')[:20]
    total_likes = ProductLike.objects.filter(product__seller=request.user).count()
    total_comments = ProductComment.objects.filter(product__seller=request.user).count()
    total_favorites = UserFavorite.objects.filter(product__seller=request.user).count()
    followers_count = SellerFollow.objects.filter(seller=request.user).count()
    chart_products = products_annotated[:10]
    return render(request, 'shop/seller_dashboard.html', {
        'stats': stats,
        'products': products_annotated[:5],
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_favorites': total_favorites,
        'followers_count': followers_count,
        'chart_products': chart_products,
    })


@login_required
def seller_products(request):
    """Мои товары — список всех товаров продавца"""
    profile = getattr(request.user, 'profile', None)
    if not profile or not profile.is_businessman:
        messages.warning(request, 'Доступно только для продавцов.')
        return redirect('become_seller')
    products = Product.objects.filter(seller=request.user).annotate(
        likes_count=Count('likes'),
        comments_count=Count('comments'),
        favorites_count=Count('favorites')
    ).select_related('brand', 'category').order_by('-created_at')
    paginator = Paginator(products, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'shop/seller_products.html', {'page_obj': page_obj})


@login_required
def seller_brand(request):
    """Магазин и мои бренды — данные компании + бренды товаров"""
    profile = getattr(request.user, 'profile', None)
    if not profile or not profile.is_businessman:
        messages.warning(request, 'Доступно только для продавцов.')
        return redirect('become_seller')

    owned_brands = Brand.objects.filter(owner=request.user).order_by('name')

    if request.method == 'POST':
        action = request.POST.get('action', 'save_shop')
        if action == 'save_shop':
            profile.company_name = (request.POST.get('company_name') or '')[:200]
            profile.phone = (request.POST.get('phone') or '')[:30]
            profile.save()
            messages.success(request, 'Данные магазина сохранены.')
        elif action == 'add_brand':
            name = (request.POST.get('brand_name') or '').strip()
            if name:
                Brand.objects.get_or_create(name=name, owner=request.user)
                messages.success(request, f'Бренд «{name}» добавлен.')
            else:
                messages.warning(request, 'Введите название бренда.')
        elif action == 'delete_brand':
            bid = request.POST.get('brand_id')
            if bid and bid.isdigit():
                Brand.objects.filter(pk=int(bid), owner=request.user).delete()
                messages.success(request, 'Бренд удалён.')
        return redirect('seller_brand')

    return render(request, 'shop/seller_brand.html', {
        'profile': profile,
        'owned_brands': owned_brands,
    })


@login_required
def chat_list(request):
    """Список чатов пользователя"""
    chat_ids = ChatParticipant.objects.filter(user=request.user).values_list('chat_id', flat=True)
    chats = Chat.objects.filter(pk__in=chat_ids).select_related('product').prefetch_related('participants__user', 'messages')
    for chat in chats:
        chat.last_message = chat.messages.last()
        other = chat.participants.exclude(user=request.user).first()
        chat.other_user = other.user if other else None
    profile = getattr(request.user, 'profile', None)
    template = 'shop/chat_list_seller.html' if profile and profile.is_businessman else 'shop/chat_list.html'
    return render(request, template, {'chats': chats})


@login_required
def chat_detail(request, pk):
    """Просмотр чата и отправка сообщений"""
    chat = get_object_or_404(Chat.objects.select_related('product', 'product__seller').prefetch_related('participants', 'messages'), pk=pk)
    if not chat.participants.filter(user=request.user).exists():
        return redirect('chat_list')
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(chat=chat, sender=request.user, text=text)
            other = chat.participants.exclude(user=request.user).first()
            if other:
                Notification.objects.create(
                    user=other.user,
                    ntype=Notification.TYPE_CHAT,
                    title=f'{request.user.username}: {text[:50]}{"..." if len(text) > 50 else ""}',
                    link=reverse('chat_detail', args=[pk])
                )
            return redirect('chat_detail', pk=pk)
    other = chat.participants.exclude(user=request.user).first()
    chat.other_user = other.user if other else None
    chat.messages.exclude(sender=request.user).update(is_read=True)
    profile = getattr(request.user, 'profile', None)
    template = 'shop/chat_detail_seller.html' if profile and profile.is_businessman else 'shop/chat_detail.html'
    return render(request, template, {'chat': chat})


@login_required
def message_edit(request, pk):
    """Редактирование своего сообщения"""
    msg = get_object_or_404(Message.objects.select_related('chat'), pk=pk)
    if msg.sender != request.user:
        return redirect('chat_detail', pk=msg.chat_id)
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            from django.utils import timezone
            msg.text = text
            msg.edited_at = timezone.now()
            msg.save()
        return redirect('chat_detail', pk=msg.chat_id)
    return render(request, 'shop/message_edit.html', {'msg': msg})


@login_required
def message_delete(request, pk):
    """Удаление своего сообщения"""
    msg = get_object_or_404(Message.objects.select_related('chat'), pk=pk)
    if msg.sender != request.user:
        return redirect('chat_detail', pk=msg.chat_id)
    chat_pk = msg.chat_id
    msg.delete()
    return redirect('chat_detail', pk=chat_pk)


@login_required
def chat_start(request):
    """Начать общий чат"""
    return _chat_start(request, product_id=None)


@login_required
def chat_start_product(request, pk):
    """Начать чат о товаре"""
    return _chat_start(request, product_id=pk)


def _chat_start(request, product_id=None):
    """Начать чат (о товаре или общий)"""
    product = get_object_or_404(Product, pk=product_id) if product_id else None
    User = get_user_model()
    other = product.seller if product and product.seller else User.objects.filter(is_superuser=True).first()
    if not other or other == request.user:
        other = User.objects.exclude(pk=request.user.pk).first()
    if not other:
        messages.warning(request, 'Пока не с кем начать чат. Зарегистрируйте другого пользователя или дождитесь появления других продавцов.')
        return redirect(reverse('product_detail', args=[product.pk]) if product else reverse('home'))
    existing = Chat.objects.filter(
        product=product,
        participants__user=request.user,
    ).filter(participants__user=other).distinct().first()
    if existing:
        return redirect('chat_detail', pk=existing.pk)
    chat = Chat.objects.create(product=product)
    ChatParticipant.objects.bulk_create([
        ChatParticipant(chat=chat, user=request.user),
        ChatParticipant(chat=chat, user=other),
    ])
    return redirect('chat_detail', pk=chat.pk)


def logout_view(request):
    """Выход из аккаунта — поддерживает GET для ссылок, редирект на главную"""
    logout(request)
    return redirect('home')


@login_required
def notifications_list(request):
    """Список уведомлений"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:50]
    return render(request, 'shop/notifications.html', {'notifications': notifications})


@login_required
def notification_read(request, pk):
    """Отметить уведомление прочитанным и перейти по ссылке"""
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect('notifications_list')


@login_required
def follow_seller(request, pk):
    """Подписаться на продавца"""
    seller = get_object_or_404(get_user_model(), pk=pk)
    if seller.id == request.user.id:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    SellerFollow.objects.get_or_create(user=request.user, seller=seller)
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url or '/')


@login_required
def unfollow_seller(request, pk):
    """Отписаться от продавца"""
    SellerFollow.objects.filter(user=request.user, seller_id=pk).delete()
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url or '/')


@login_required
def profile_view(request):
    """Страница профиля пользователя"""
    profile = getattr(request.user, 'profile', None)
    favorites_count = UserFavorite.objects.filter(user=request.user).count()
    likes_count = ProductLike.objects.filter(user=request.user).count()
    products_count = 0
    if profile and profile.is_businessman:
        products_count = Product.objects.filter(seller=request.user).count()

    template = 'shop/profile_seller.html' if profile and profile.is_businessman else 'shop/profile.html'
    return render(request, template, {
        'profile': profile,
        'favorites_count': favorites_count,
        'likes_count': likes_count,
        'products_count': products_count,
    })


def support_view(request):
    """Страница поддержки"""
    return render(request, 'shop/support.html')
