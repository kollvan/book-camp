from django import template

from goods.models import Category
from inventory.models import Inventory

register = template.Library()

@register.simple_tag()
def get_available_categories():
    return Category.objects.all()