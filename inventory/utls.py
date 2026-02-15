from dataclasses import dataclass

from django.db.models import QuerySet

from goods.utls import FilterParams, FilterQueryset, Filters


@dataclass
class InventoryFilterParams(FilterParams):
    status: str = None
    category: str = None


@dataclass
class InventoryFilters(Filters):
    filter_field_tags: str = 'product__tags__slug__in'
    filter_field_author: str = 'product__author__slug__in'
    filter_field_years_of_publication: str = 'product__year_of_publication__range'


class FilterQuerysetForInventory(FilterQueryset):
    def get_filter_queryset(self, params: InventoryFilterParams, filters: Filters = InventoryFilters()) -> QuerySet:
        return super().get_filter_queryset(params, filters)

    def filter_status(self, status, **kwargs) -> None:
        if status:
            self.queryset = self.queryset.filter(status=status)

    def filter_category(self, category, **kwargs) -> None:
        if category:
            self.queryset = self.queryset.filter(product__category__slug=category)
