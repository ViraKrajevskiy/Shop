(function() {
    document.addEventListener('DOMContentLoaded', function() {
        // User dropdown — position:fixed чтобы не обрезалось в скроллируемом навбаре
        const userDropdownEl = document.querySelector('.nav-user-dropdown [data-bs-toggle="dropdown"]');
        if (userDropdownEl && typeof bootstrap !== 'undefined') {
            const existing = bootstrap.Dropdown.getInstance(userDropdownEl);
            if (existing) existing.dispose();
            new bootstrap.Dropdown(userDropdownEl, {
                popperConfig: { strategy: 'fixed' }
            });
        }

        // Theme toggle (theme applied in head inline script)
        const btn = document.querySelector('.theme-toggle');
        if (btn) btn.addEventListener('click', function() {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            document.documentElement.setAttribute('data-theme', isDark ? '' : 'dark');
            localStorage.setItem('theme', isDark ? 'light' : 'dark');
        });
    });

    const trans = {
        ru: {
            search_btn: 'Найти',
            post_ad: 'Подать объявление',
            login: 'Войти',
            logout: 'Выйти',
            chats: 'Чаты',
            create_title: 'Подать объявление',
            create_desc: 'Разместите объявление о продаже одежды. Форма в разработке.',
            back: '← Назад',
            profile: 'Профиль',
            notifications: 'Уведомления',
            support: 'Поддержка',
            favorites_title: 'Избранное',
            favorites_empty: 'В избранном пока ничего нет',
            go_catalog: 'Перейти в каталог',
            search_placeholder: 'Поиск...'
        },
        en: {
            search_btn: 'Search',
            post_ad: 'Post listing',
            login: 'Log in',
            logout: 'Log out',
            chats: 'Chats',
            create_title: 'Post listing',
            create_desc: 'Place your clothing listing. Form coming soon.',
            back: '← Back',
            profile: 'Profile',
            notifications: 'Notifications',
            support: 'Support',
            favorites_title: 'Favorites',
            favorites_empty: 'Nothing in favorites yet',
            go_catalog: 'Go to catalog',
            search_placeholder: 'Search...'
        }
    };
    let lang = localStorage.getItem('lang') || 'ru';
    document.documentElement.lang = lang === 'en' ? 'en' : 'ru';
    const label = document.getElementById('langLabel');
    if (label) label.textContent = lang.toUpperCase();
    function applyLang() {
        const t = trans[lang] || trans.ru;
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const k = el.getAttribute('data-i18n');
            if (t[k]) el.textContent = t[k];
        });
        const q = document.querySelector('[name="q"]');
        if (q) q.setAttribute('placeholder', t.search_placeholder || '');
    }
    applyLang();
    document.querySelectorAll('.lang-opt').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            lang = this.dataset.lang;
            localStorage.setItem('lang', lang);
            document.documentElement.lang = lang === 'en' ? 'en' : 'ru';
            if (label) label.textContent = lang.toUpperCase();
            applyLang();
        });
    });

    // Избранное — AJAX
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a.fav-btn, a[data-fav-toggle]');
        if (!link || link.hasAttribute('data-fav-loading')) return;
        const href = link.getAttribute('href');
        if (!href || (!href.includes('/favorites/add/') && !href.includes('/favorites/remove/'))) return;
        e.preventDefault();
        link.setAttribute('data-fav-loading', '1');
        const origHtml = link.innerHTML;
        link.innerHTML = '<i class="bi bi-arrow-repeat spinner"></i>';
        fetch(href, {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            credentials: 'same-origin'
        }).then(r => r.json()).then(data => {
            if (!data.ok) return;
            document.querySelectorAll('.favorites-btn').forEach(btn => {
                const BadgeClass = 'favorites-badge';
                let badge = btn.querySelector('.' + BadgeClass);
                if (data.count > 0) {
                    if (!badge) {
                        badge = document.createElement('span');
                        badge.className = BadgeClass;
                        btn.appendChild(badge);
                    }
                    badge.textContent = data.count;
                    badge.style.display = '';
                } else if (badge) badge.style.display = 'none';
            });

            if (link.classList.contains('fav-btn')) {
                if (data.action === 'add') {
                    link.href = href.replace('/favorites/add/', '/favorites/remove/');
                    link.innerHTML = '<i class="bi bi-heart-fill"></i>';
                    link.title = 'Убрать из избранного';
                } else {
                    link.href = href.replace('/favorites/remove/', '/favorites/add/');
                    link.innerHTML = '<i class="bi bi-heart"></i>';
                    link.title = 'В избранное';
                }
            } else {
                const wrap = link.closest('[data-fav-buttons]');
                if (wrap) {
                    if (data.action === 'add') {
                        link.href = href.replace('/favorites/add/', '/favorites/remove/');
                        link.className = 'btn btn-outline-danger';
                        link.innerHTML = '<i class="bi bi-heart-fill me-1"></i>Убрать из избранного';
                    } else {
                        link.href = href.replace('/favorites/remove/', '/favorites/add/');
                        link.className = 'btn btn-outline-secondary';
                        link.innerHTML = '<i class="bi bi-heart me-1"></i>В избранное';
                    }
                } else link.innerHTML = origHtml;
            }
        }).catch(() => { link.innerHTML = origHtml; }).finally(() => {
            link.removeAttribute('data-fav-loading');
        });
    });

    // Лайки — AJAX
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a.like-btn, a[data-like-toggle]');
        if (!link || link.hasAttribute('data-like-loading')) return;
        const href = link.getAttribute('href');
        if (!href || !href.includes('/like/')) return;
        e.preventDefault();
        link.setAttribute('data-like-loading', '1');
        const countSpan = link.querySelector('.product-stat-count');
        const icon = link.querySelector('i');
        const origCount = countSpan ? countSpan.textContent : '0';
        if (icon) icon.className = 'bi bi-arrow-repeat spinner';
        fetch(href, {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            credentials: 'same-origin'
        }).then(r => {
            if (r.ok && r.headers.get('content-type')?.includes('application/json')) return r.json();
            throw new Error('Not JSON');
        }).then(data => {
            if (!data.ok) return;
            if (countSpan) countSpan.textContent = data.count;
            if (data.action === 'add') {
                link.classList.add('liked');
                if (icon) icon.className = 'bi bi-heart-fill';
            } else {
                link.classList.remove('liked');
                if (icon) icon.className = 'bi bi-heart';
            }
        }).catch(() => {
            if (countSpan) countSpan.textContent = origCount;
            if (icon) icon.className = link.classList.contains('liked') ? 'bi bi-heart-fill' : 'bi bi-heart';
        }).finally(() => link.removeAttribute('data-like-loading'));
    });
})();
