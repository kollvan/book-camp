from django.http import HttpResponse
from django.shortcuts import render

from inventory.models import Inventory


# Create your views here.
def inventory(request):
    inventory = Inventory.objects.filter(user=request.user.pk)

    context={
        'title':'Инвентарь',
        'inventory': inventory,
    }
    return render(request, 'inventory/inventory.html', context=context)