from django.db.models import Count
from django.views.generic import ListView, DetailView

from common.mixin.generic import CacheViewMixin, SelectRelatedMixin
from common.mixin.search import SearchMixin
from goods import constans
from goods.constans import DEFAULT_CACHE_TIME
from goods.models import Product, Category
from goods.utls import RangeYear, get_current_year, FilterParams, FilterQueryset


# Create your views here.
class CatalogView(SearchMixin, SelectRelatedMixin, ListView):
    template_name = 'goods/catalog.html'
    context_object_name = 'products'
    search_fields = {
        'name': 'name',
        'description': 'description',
    }
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
            'is_high_rank': context['view'].request.GET.get('is_high_rank', None),
            'category_slug': self.kwargs['category_slug'],
        }
        context.update(extra_context)
        return context

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        products = super().get_queryset()

        if category_slug != 'all':
            products = super().get_queryset().filter(category__slug=category_slug)

        years = RangeYear(
            self.request.GET.get('year_from', '0'),
            self.request.GET.get('year_to', get_current_year())
        )

        params = FilterParams(
            tags=self.request.GET.getlist('tags', None),
            authors=self.request.GET.getlist('authors', None),
            years=years,
            ordering=self.request.GET.get('ordering', None),
            is_high_rank=self.request.GET.get('is_high_rank', None),
        )

        queryset_filter = FilterQueryset(products)
        return queryset_filter.get_filter_queryset(params)


class ProductView(CacheViewMixin, SelectRelatedMixin, DetailView):
    related_fields = ['author']
    prefetch_related_fields = ['tags']
    template_name = 'goods/product.html'
    model = Product
    slug_url_kwarg = 'product_slug'
    cache_time = DEFAULT_CACHE_TIME * 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product'].name
        context['reviews_page_size'] = constans.REVIEWS_PAGE_SIZE
        return context


class CategoriesView(SearchMixin, ListView):
    model = Category
    template_name = 'goods/categories.html'
    context_object_name = 'main_categories'
    paginate_by = 20
    extra_context = {'title': 'Bookcamp - Категории'}
    search_fields = {'name': 'name'}

    def get_queryset(self):
        categories = super().get_queryset()
        return categories.annotate(number=Count('product__pk')).order_by('-number')
