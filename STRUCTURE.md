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

- `base.html` — основной layout
- `home.html` — главная / каталог
- `product_detail.html` — страница товара
- `favorites.html` — избранное
- `seller_layout.html`, `seller_dashboard.html` и др. — кабинет продавца
- `chat_list.html`, `chat_detail.html` — чаты
- `login.html`, `register.html`, `become_seller.html` — авторизация
