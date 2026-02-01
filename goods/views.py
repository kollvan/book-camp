from django.views.generic import ListView, DetailView

from common.mixin.generic import CacheViewMixin, SelectRelatedMixin
from goods.models import Product
from goods.utls import RangeYear, get_current_year, search, FilterParams, FilterQueryset


# Create your views here.
class CatalogView(SelectRelatedMixin, ListView):
    template_name = 'goods/catalog.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 12
    related_fields = ['author']
    prefetch_related_fields = ['tags']
    extra_context = {
        'title': 'BookCamp - Каталог',
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            'ordering': context['view'].request.GET.get('ordering', None),
            'selected_tags': context['view'].request.GET.getlist('tags', None),
            'selected_authors': context['view'].request.GET.getlist('authors', None),
            'year_from': context['view'].request.GET.get('year_from', None),
            'year_to': context['view'].request.GET.get('year_to', None),
            'category_slug': self.kwargs['category_slug'],
        }
        context.update(extra_context)
        return context

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']

        if query := self.request.GET.get('q', None):
            products = search(query)
        elif category_slug == 'all':
            products = super().get_queryset()
        else:
            products = super().get_queryset().filter(category__slug=category_slug)

        years = RangeYear(
            self.request.GET.get('year_from', '0'),
            self.request.GET.get('year_to', get_current_year())
        )

        params = FilterParams(
            tags=self.request.GET.getlist('tags', None),
            authors=self.request.GET.getlist('authors', None),
            years=years,
            ordering=self.request.GET.get('ordering', None)
        )
        queryset_filter = FilterQueryset(products, params)
        products = queryset_filter.get_filter_queryset()

        return products


class ProductView(CacheViewMixin, SelectRelatedMixin, DetailView):
    related_fields = ['author']
    prefetch_related_fields = ['tags']
    template_name = 'goods/product.html'
    model = Product
    slug_url_kwarg = 'product_slug'
    cache_time = 360

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product'].name
        return context
