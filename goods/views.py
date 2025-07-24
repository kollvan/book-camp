from django.contrib.postgres.search import SearchVector
from django.views.generic import ListView, DetailView

from goods.models import Product
from goods.utls import RangeYear, get_current_year, search


# Create your views here.
class CatalogView(ListView):
    template_name = 'goods/catalog.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 15
    extra_context = {
        'title': 'BookCamp - Каталог',
    }
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            'ordering': context['view'].request.GET.get('ordering', None),
            'selected_tags': context['view'].request.GET.getlist('tags', None),
            'selected_authors':context['view'].request.GET.getlist('authors', None),
            'year_from':context['view'].request.GET.get('year_from', None),
            'year_to':context['view'].request.GET.get('year_to', None),
            'category_slug':self.kwargs['category_slug'],
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

        if tags := self.request.GET.getlist('tags', None):
            products = products.filter(tags__slug__in=tags).distinct()

        if authors := self.request.GET.getlist('authors', None):
            products = products.filter(author__slug__in=authors)
        current_year = get_current_year()

        years = RangeYear(
            self.request.GET.get('year_from', '0'),
            self.request.GET.get('year_to', current_year)
        )

        if not years.is_default():
            products = products.filter(year_of_publication__range=(years.year_from, years.year_to))


        if self.request.GET.get('ordering', None):
            products = products.order_by(self.request.GET.get('ordering', None))
        return products.select_related('author').prefetch_related('tags')



class ProductView(DetailView):
    template_name = 'goods/product.html'
    model = Product
    slug_url_kwarg = 'product_slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product'].name
        return context
