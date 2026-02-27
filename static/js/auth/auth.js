(function() {
    document.addEventListener('DOMContentLoaded', function() {
        /* Показать/скрыть пароль */
        document.querySelectorAll('.btn-password-toggle').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var id = this.getAttribute('data-target');
                var input = document.getElementById(id);
                if (!input) return;
                var visible = this.classList.toggle('is-visible');
                input.type = visible ? 'text' : 'password';
                this.setAttribute('aria-label', visible ? 'Скрыть пароль' : 'Показать пароль');
            });
        });

        /* Показать поля продавца при выборе роли */
        var sellerFields = document.getElementById('sellerFields');
        var roleRadios = document.querySelectorAll('input[name="role"]');
        if (sellerFields && roleRadios.length) {
            function toggleSellerFields() {
                var businessman = document.querySelector('input[name="role"][value="businessman"]');
                sellerFields.style.display = businessman && businessman.checked ? 'block' : 'none';
            }
            roleRadios.forEach(function(r) { r.addEventListener('change', toggleSellerFields); });
            toggleSellerFields();
        }

        var page = document.querySelector('.auth-page');
        if (!page) return;

        var content = document.querySelector('.auth-card');
        if (!content) return;

        function doTransition(e, hrefOrForm) {
            if (document.body.classList.contains('auth-transitioning')) return;
            document.body.classList.add('auth-transitioning');
            content.style.animation = 'auth-card-exit 0.3s ease forwards';

            setTimeout(function() {
                if (typeof hrefOrForm === 'string') {
                    window.location.href = hrefOrForm;
                } else if (hrefOrForm && hrefOrForm.submit) {
                    hrefOrForm.submit();
                }
            }, 280);
        }

        document.querySelectorAll('.auth-card a[href]').forEach(function(a) {
            var href = a.getAttribute('href');
            if (href && href !== '#' && !a.hasAttribute('data-no-transition')) {
                a.addEventListener('click', function(e) {
                    e.preventDefault();
                    doTransition(e, href);
                });
            }
        });

        document.querySelectorAll('.auth-card form').forEach(function(form) {
            form.addEventListener('submit', function(e) {
                if (form.checkValidity && !form.checkValidity()) return;
                e.preventDefault();
                var btn = form.querySelector('button[type="submit"]');
                if (btn) {
                    btn.disabled = true;
                    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Отправка...';
                }
                doTransition(e, form);
            });
        });
    });
})();
