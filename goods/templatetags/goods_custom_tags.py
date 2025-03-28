from django import template
from django.utils.http import urlencode

from goods.models import Category, Tag, Author
from inventory.models import Inventory

register = template.Library()
@register.simple_tag(takes_context=True)
def append_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    if not kwargs.get('tags', None):
        query['tags'] = context['request'].GET.getlist('tags', [])
    if not kwargs.get('authors', None):
        query['authors'] = context['request'].GET.getlist('authors', [])
    return urlencode(query, doseq=True)

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_all_tags():
    return Tag.objects.all()

@register.simple_tag()
def get_authors(category_slug):
    if category_slug == 'all':
        return Author.objects.all()[:10]
    return Author.objects.filter(product__category__slug=category_slug)[:10]

@register.simple_tag()
def get_product_status(product_pk):
    try:
        return Inventory.objects.get(product=product_pk).status
    except Inventory.DoesNotExist:
        return None

