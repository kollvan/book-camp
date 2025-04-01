from django import template

from goods.models import Category, Tag, Author
from inventory.models import Inventory

register = template.Library()

@register.simple_tag()
def get_available_categories():
    return Category.objects.all()

@register.simple_tag()
def get_available_tags():
    return Tag.objects.all()

@register.simple_tag()
def get_available_authors():
    return Author.objects.all()
