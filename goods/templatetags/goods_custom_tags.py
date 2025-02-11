from django import template
from django.utils.http import urlencode

from goods.models import Category, Tag

register = template.Library()
@register.simple_tag(takes_context=True)
def append_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_all_tags():
    return Tag.objects.all()