from django.shortcuts import render
from django.views.decorators.cache import cache_page

from bookcamp import settings


# Create your views here.

def index(request):
    context = {
        'title': 'BookCamp - Главная страница',
    }
    return render(request, 'main/index.html', context)

def about(request):
    return render(request, 'main/about.html')