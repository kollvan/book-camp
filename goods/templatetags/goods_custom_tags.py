from django import template
from django.db.models import Q
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
        return Author.objects.all()
    return Author.objects.filter(product__category__slug=category_slug)

@register.simple_tag()
def get_inventory_data(products, user_id):
    allowed_id = {item['id'] for item in products.values('id')}
    try:
        inventory_items = {
            item.product_id : item.status for item in Inventory.objects.filter(Q(product__in=allowed_id) & Q(user=user_id))
        }
        return inventory_items
    except Inventory.DoesNotExist:
        return None
@register.simple_tag()
def get_item(collection:dict, key:str):
    return collection.get(key, None)

@register.simple_tag()
def get_product_status(product_id, user_id):
    try:
        return Inventory.objects.get(Q(product_id=product_id)&Q(user=user_id)).status
    except Inventory.DoesNotExist:
        return None

