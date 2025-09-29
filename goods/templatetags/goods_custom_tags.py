from typing import Any

from django import template
from django.db.models import Q, Avg, QuerySet
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
def get_user_data(product_pk, user_pk):
    try:
        elem = Inventory.objects.get(Q(product__pk=product_pk) & Q(user__pk=user_pk))
        result = {
            'rank':elem.rank,
            'status':elem.status,
        }
        return result
    except Inventory.DoesNotExist:
        return None

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
def get_avg_ranks(products):
    try:
        qs = Inventory.objects.filter(Q(product__pk__in=products) & ~Q(rank=0) ).values('product__pk').annotate(Avg('rank'))
        dict_inventory = {
            item['product__pk'] : item['rank__avg'] for item in qs
        }
        return dict_inventory
    except Inventory.DoesNotExist:
        return {}

@register.simple_tag()
def get_avg_rank(product_pk):
    try:
        qs = Inventory.objects.filter(product__pk=product_pk)
        value = qs.values('product__pk').annotate(Avg('rank')).values('rank__avg').get()
        return round(value['rank__avg'], 2)
    except Inventory.DoesNotExist:
        return 0.00
@register.simple_tag()
def get_item(collection:dict, key:str, default=None):
    return collection.get(key, default)



