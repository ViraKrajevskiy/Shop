# Структура проекта Shop

## Статические файлы (static/)

### CSS
```
css/
├── layout/
│   └── base.css      # Дизайн-система, навбар, базовые стили
├── pages/
│   ├── home.css      # Каталог, карточки товаров, sidebar
│   ├── product.css   # Страница товара
│   ├── favorites.css # Страница избранного
│   └── pages.css     # Create listing и прочие страницы
├── auth/
│   └── auth.css      # Логин, регистрация, become_seller
├── seller/
│   └── seller.css    # Боковая панель продавца
└── chat/
    └── chat.css      # Чаты, сообщения
```

### JavaScript
```
js/
├── core/
│   └── base.js       # Тема, язык, избранное, лайки (AJAX)
├── auth/
│   └── auth.js       # Формы авторизации, анимации
└── chat/
    └── chat.js       # Скролл чата
```

## Шаблоны (templates/shop/)

```
shop/
├── base.html              # Основной layout (наследуют все)
├── auth/
│   ├── login.html
│   ├── register.html
│   └── become_seller.html
├── pages/
│   ├── home.html          # Главная / каталог
│   ├── product_detail.html
│   ├── favorites.html
│   ├── profile.html
│   ├── notifications.html
│   └── support.html
├── seller/
│   ├── seller_layout.html # Layout кабинета продавца
│   ├── seller_dashboard.html
│   ├── seller_products.html
│   ├── seller_brand.html
│   ├── profile_seller.html
│   ├── create_listing.html
│   ├── chat_list_seller.html
│   └── chat_detail_seller.html
└── chat/
    ├── chat_list.html
    ├── chat_detail.html
    └── message_edit.html
```
