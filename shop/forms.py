from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Brand, Category, Product, UserProfile

User = get_user_model()


class RegisterForm(UserCreationForm):
    """Регистрация — только как покупатель. Статус продавца через заявку."""

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            UserProfile.objects.get_or_create(user=user, defaults={'role': UserProfile.ROLE_USER})
        return user


class BecomeSellerForm(forms.Form):
    """Заявка на статус продавца (для уже зарегистрированных)"""
    company_name = forms.CharField(
        label='Название компании / магазина',
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Например: ООО "Стиль"', 'class': 'form-control'})
    )
    phone = forms.CharField(
        label='Телефон для связи',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '+7 999 123-45-67', 'class': 'form-control'})
    )
    comment = forms.CharField(
        label='Комментарий (по желанию)',
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Расскажите о вашем магазине...', 'class': 'form-control', 'rows': 3})
    )


class ProductForm(forms.ModelForm):
    """Форма подачи объявления о товаре. Бренд выбирается: свой / другой / добавить новый."""

    BRAND_MY = 'my'
    BRAND_EXISTING = 'existing'
    BRAND_NEW = 'new'

    brand_mode = forms.ChoiceField(
        label='Бренд товара',
        choices=[],  # заполняется в __init__
        widget=forms.RadioSelect(attrs={'class': 'brand-mode-radio'})
    )
    brand_my_id = forms.ModelChoiceField(
        queryset=Brand.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    brand_existing_id = forms.ModelChoiceField(
        queryset=Brand.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    brand_new_name = forms.CharField(
        label='Название нового бренда',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'})
    )

    def __init__(self, *args, user=None, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.order_by('name')
        self.fields['category'].empty_label = '— Выберите тип товара —'
        self.fields['category'].label = 'Тип товара'

        owned = Brand.objects.filter(owner=self._user).order_by('name') if self._user else []
        all_brands = Brand.objects.order_by('name')

        choices = []
        if owned:
            choices.append((self.BRAND_MY, 'Мой бренд'))
        choices.append((self.BRAND_EXISTING, 'Выбрать из списка'))
        choices.append((self.BRAND_NEW, 'Добавить новый бренд'))

        self.fields['brand_mode'].choices = choices
        if owned and not self.initial.get('brand_mode'):
            self.initial['brand_mode'] = self.BRAND_MY
        elif not owned and not self.initial.get('brand_mode'):
            self.initial['brand_mode'] = self.BRAND_EXISTING
        self.fields['brand_my_id'].queryset = owned
        self.fields['brand_my_id'].empty_label = '— Выберите —'
        self.fields['brand_existing_id'].queryset = all_brands
        self.fields['brand_existing_id'].empty_label = '— Выберите бренд —'
        self._owned_brands = list(owned)
        self._all_brands = list(all_brands)

    def clean(self):
        data = super().clean()
        mode = data.get('brand_mode')
        brand_my_id = data.get('brand_my_id')
        brand_existing_id = data.get('brand_existing_id')
        brand_new_name = (data.get('brand_new_name') or '').strip()

        if mode == self.BRAND_MY:
            if not brand_my_id:
                self.add_error('brand_mode', 'Выберите ваш бренд')
                return data
            data['_resolved_brand'] = brand_my_id
        elif mode == self.BRAND_EXISTING:
            if not brand_existing_id:
                self.add_error('brand_mode', 'Выберите бренд из списка')
                return data
            data['_resolved_brand'] = brand_existing_id
        elif mode == self.BRAND_NEW:
            if not brand_new_name:
                self.add_error('brand_new_name', 'Введите название бренда')
                return data
            data['_brand_to_create'] = brand_new_name
        return data

    class Meta:
        model = Product
        fields = ('name', 'model', 'category', 'image', 'description', 'price', 'is_vip', 'is_new')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Куртка демисезонная'
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Артикул или модель (необязательно)'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите товар: размер, состав, состояние и т.д.',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
                'step': '100'
            }),
            'is_vip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_new': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
