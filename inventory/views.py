from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpRequest, Http404, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView

from goods.utls import get_current_year, RangeYear
from inventory.models import Inventory
from inventory.utls import FilterQuerysetForInventory, InventoryFilterParams


# Create your views here.
class InventoryView(LoginRequiredMixin,ListView):
    template_name = 'inventory/inventory.html'
    extra_context = {'title':'Bookcamp Инвентарь - ',}
    context_object_name = 'inventory'
    paginate_by = 20
    model = Inventory
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] += context['view'].request.user.username
        extr_context = {
            'selected_status':context['view'].request.GET.get('status', None),
            'selected_category':context['view'].request.GET.get('category', None),
            'selected_ordering':context['view'].request.GET.get('ordering', None),
            'selected_tags':context['view'].request.GET.getlist('tags', None),
            'selected_authors':context['view'].request.GET.getlist('authors', None),
            'year_to':context['view'].request.GET.get('year_to', None),
            'year_from':context['view'].request.GET.get('year_from', None),

        }
        print(extr_context)
        context.update(extr_context)
        return context
    def get_queryset(self):
        inventory = super().get_queryset().filter(user=self.request.user.pk)

        order_fields = {
            'author':'product__author__name',
            'name':'product__name',
            'status':'-status',
        }

        years = RangeYear(
            self.request.GET.get('year_from', '0'),
            self.request.GET.get('year_to', get_current_year())
        )

        params = InventoryFilterParams(
            tags=self.request.GET.getlist('tags', None),
            authors=self.request.GET.getlist('authors', None),
            years=years,
            ordering=order_fields.get(self.request.GET.get('ordering', None), None),
            status=self.request.GET.get('status', None),
            category=self.request.GET.get('category', None),
        )

        queryset_filter = FilterQuerysetForInventory(inventory, params)
        inventory = queryset_filter.get_filter_queryset()
        return inventory.select_related('product__author').prefetch_related('product__tags')

class UserData(View):
    def get(self, request:HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            get_object_or_404(Inventory, user=request.user, product__slug=self.kwargs['product_slug'])
            print(request.user, self.kwargs['product_slug'], sep='\n')

            context = {
                'product_status': 1,
                'rank': 0,
                'product_slug': self.kwargs['product_slug'],
            }
            html_response = render_to_string('../templates/includes/user_data_product.html', context)
            return JsonResponse({'user_data' : html_response})

        return HttpResponseBadRequest()