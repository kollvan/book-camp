from django.core.paginator import Paginator
from django.shortcuts import render

from goods.models import Product
from inventory.models import Inventory


# Create your views here.

def catalog(request, category_slug=None):
    if category_slug == 'all':
      products = Product.objects.all()
    else:
        products = Product.objects.filter(category__slug=category_slug)

    tags = request.GET.getlist('tags', None)
    if tags:
        products = products.filter(tags__slug__in=tags)

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)

    context = {
        'title': 'Каталог',
        'products': page_products,
    }

    return render(request, 'goods/catalog.html', context=context)

def product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    context = {
        'title': product.name,
        'product': product,
    }
    return render(request, 'goods/product.html', context=context)