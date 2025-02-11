from django.core.paginator import Paginator
from django.shortcuts import render

from goods.models import Product


# Create your views here.

def catalog(request):
    paginator = Paginator(Product.objects.all() , 3)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
    context = {
        'title': 'Каталог',
        'products': page_products,
    }

    return render(request, 'goods/catalog.html', context=context)

def product(request, product_slug):
    product = Product.objects.filter(slug=product_slug)
    context = {
        'title': product.name,
        'product': product,
    }
    return render(request, 'goods/product.html', context=context)