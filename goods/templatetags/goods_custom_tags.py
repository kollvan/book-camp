from functools import wraps
from typing import Any, Hashable, Callable

from django import template
from django.core.cache import cache
from django.db.models import Q, Avg, QuerySet, Count
from django.template import Context
from django.utils.http import urlencode

from goods.models import Category, Tag, Author
from inventory.models import Inventory

register = template.Library()


def cache_custom_tag(cache_key: Any, cache_time: int = 60) -> Callable:
    def func_decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(category_slug: str, *args, **kwargs) -> QuerySet:
            queryset = cache.get_or_set(
                f'{cache_key}_{category_slug}',
                func(category_slug, *args, **kwargs),
                cache_time
            )
            return queryset

        return wrapper

    return func_decorator


@register.simple_tag(takes_context=True)
def append_params(context: Context, **kwargs) -> str:
    query = context['request'].GET.dict()
    query.update(kwargs)
    if not kwargs.get('tags', None):
        query['tags'] = context['request'].GET.getlist('tags', [])
    if not kwargs.get('authors', None):
        query['authors'] = context['request'].GET.getlist('authors', [])
    return urlencode(query, doseq=True)


@register.simple_tag()
def get_categories() -> QuerySet:
    return Category.objects.all()


@register.simple_tag()
@cache_custom_tag('category_tags')
def get_all_tags(category_slug: str) -> QuerySet:
    if category_slug == 'all':
        return Tag.objects.all()
    return Tag.objects.filter(product_tag__category__slug=category_slug).distinct()


@register.simple_tag()
@cache_custom_tag('category_authors')
def get_authors(category_slug: str) -> QuerySet:
    if category_slug == 'all':
        return Author.objects.all()
    return Author.objects.filter(product__category__slug=category_slug).distinct()


@register.simple_tag()
def get_user_data(product_pk: int, user_pk: int) -> QuerySet | None:
    try:
        elem = Inventory.objects.get(Q(product__pk=product_pk) & Q(user__pk=user_pk))
        return elem
    except Inventory.DoesNotExist:
        return None


@register.simple_tag()
def get_all_reviews(product_pk: int, user_pk: int | None = None, limit: int = 5) -> QuerySet | None:
    try:
        queryset = Inventory.objects.filter(~Q(review=None) & Q(product__pk=product_pk))
        if user_pk:
            queryset.filter(~Q(user=user_pk))
        return queryset.values('rank', 'user__username', 'review')[:limit]
    except Inventory.DoesNotExist:
        return None


@register.simple_tag()
def reviews_greater_than(product_pk: int, quantity: int = 5):
    try:
        count = Inventory.objects.filter(
            ~Q(review=None) & Q(product__pk=product_pk)
        ).aggregate(Count('id'))
        return count['id__count'] > quantity
    except Inventory.DoesNotExist:
        return False


@register.simple_tag()
def get_inventory_data(products: QuerySet, user_id: int) -> dict[int:int] | None:
    allowed_id = {item['id'] for item in products.values('id')}
    try:
        inventory_items = {
            item.product_id: item.status for item in
            Inventory.objects.filter(Q(product__in=allowed_id) & Q(user=user_id))
        }
        return inventory_items
    except Inventory.DoesNotExist:
        return None


@register.simple_tag()
def get_avg_ranks(products: list[int] | QuerySet) -> dict:
    try:
        qs = Inventory.objects.filter(Q(product__pk__in=products) & ~Q(rank=0)).values('product__pk').annotate(
            Avg('rank'))
        dict_inventory = {
            item['product__pk']: item['rank__avg'] for item in qs
        }
        return dict_inventory
    except Inventory.DoesNotExist:
        return {}


@register.simple_tag()
def get_avg_rank(product_pk: int) -> float:
    try:
        value = Inventory.objects.filter(
            Q(product__pk=product_pk) & ~Q(rank=0)
        ).aggregate(Avg('rank'))
        return round(value['rank__avg'], 2) if value['rank_avg'] else 0.00
    except Exception as e:
        return 0.00


@register.simple_tag()
def get_item(collection: dict[Hashable:Any], key: Hashable, default: Any | None = None) -> Any:
    return collection.get(key, default)
