from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from inventory.models import Inventory


# Create your views here.
class InventoryView(LoginRequiredMixin,ListView):
    template_name = 'inventory/inventory.html'
    extra_context = {'title':'Bookcamp Инвентарь - ',}
    context_object_name = 'inventory'
    paginate_by = 6
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] += context['view'].request.user.username
        return context
    def get_queryset(self):
        ordering = self.request.GET.get('ordering', None)
        inventory = Inventory.objects.filter(user=self.request.user.pk)
        order_fields = {
            'author':'product__author__name',
            'name':'product__name',
            'status':'-status',
        }
        category = self.request.GET.get('category', None)
        status = self.request.GET.get('status', None)
        self.extra_context.update(selected_status=status, selected_category=category, selected_ordering=ordering)
        if status:
            inventory = inventory.filter(status=status)
        if category:
            inventory = inventory.filter(product__category__slug=category)
        if ordering:
            inventory = inventory.order_by(order_fields[ordering])
        return inventory.select_related('product__author')
