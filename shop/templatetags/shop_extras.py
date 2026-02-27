from django import template

register = template.Library()

# Реальные фото одежды для плейсхолдеров (Unsplash, бесплатные)
CLOTHING_IMAGES = [
    'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400&q=80',  # hoodie
    'https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?w=400&q=80',  # t-shirt
    'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&q=80',  # jacket
    'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400&q=80',  # streetwear
    'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&q=80',  # jeans
    'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&q=80',  # fashion
    'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&q=80',  # outfit
    'https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?w=400&q=80',  # clothing
]


@register.simple_tag
def product_image_src(product):
    """URL картинки товара: своя или плейсхолдер одежды"""
    if product.image:
        return product.image.url
    return CLOTHING_IMAGES[product.id % len(CLOTHING_IMAGES)]


@register.simple_tag(takes_context=True)
def pagination_url(context, page_number):
    """Build URL with page param, preserving other GET params."""
    request = context['request']
    params = request.GET.copy()
    params['page'] = page_number
    return '?' + params.urlencode()
