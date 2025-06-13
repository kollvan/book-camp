
from django.views.generic import ListView, DetailView

from goods.models import Product
from goods.utls import RangeYear, get_current_year


# Create your views here.
class CatalogView(ListView):
    template_name = 'goods/catalog.html'

    context_object_name = 'products'

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
        if category_slug == 'all':
            products = Product.objects.all()
        else:
            products = Product.objects.filter(category__slug=category_slug)
        tags = self.request.GET.getlist('tags', None)
        if tags:
            products = products.filter(tags__slug__in=tags).distinct()
        authors = self.request.GET.getlist('authors', None)
        if authors:
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
