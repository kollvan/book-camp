from dataclasses import dataclass

from goods.utls import FilterParams, FilterQueryset, Filters


@dataclass
class InventoryFilterParams(FilterParams):
    status: str = None
    category: str = None


@dataclass
class InventoryFilters(Filters):
    filter_field_tags = 'product__tags__slug__in'
    filter_field_author = 'product__author__slug__in'
    filter_years_of_publication = 'product__year_of_publication__range'


class FilterQuerysetForInventory(FilterQueryset):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, filters=InventoryFilters(), **kwargs)

    def filter_status(self) -> None:
        if status := self.params.status:
            self.queryset = self.queryset.filter(status=status)

    def filter_category(self) -> None:
        if category := self.params.category:
            self.queryset = self.queryset.filter(product__category__slug=category)
