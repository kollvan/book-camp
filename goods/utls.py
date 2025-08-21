from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple

from django.contrib.postgres.search import SearchVector, SearchHeadline, SearchQuery, SearchRank
from django.db.models import QuerySet

from goods.models import Product


def get_current_year() -> str:
    return str(datetime.now().year)


class RangeYear(NamedTuple):
    year_from: str = '0'
    year_to: str = get_current_year()

    def is_default(self) -> bool:
        return self.year_from == '0' and self.year_to == get_current_year()


def search(query: str) -> QuerySet:
    search_vector = SearchVector('name', 'description')
    query = SearchQuery(query)
    records = Product.objects.annotate(rank=SearchRank(search_vector, query)).filter(rank__gt=0).order_by('-rank')

    records = records.annotate(headline=SearchHeadline('name', query,
                                                       start_sel='<span class="select">',
                                                       stop_sel='</span>'))
    records = records.annotate(bodyline=SearchHeadline('description', query,
                                                       start_sel='<span class="select">',
                                                       stop_sel='</span>'))
    return records


@dataclass
class FilterParams:
    tags: list = None
    authors: list = None
    years: RangeYear = None
    ordering: str = None


@dataclass
class Filters:
    filter_field_tags = 'tags__slug__in'
    filter_field_author = 'author__slug__in'
    filter_field_years_of_publication = 'year_of_publication__range'


class FilterQueryset:
    def __init__(self, queryset: QuerySet, params: FilterParams, filters: Filters = Filters()):
        self.queryset = queryset
        self.params = params
        self.filters = filters

    def get_filter_queryset(self) -> QuerySet:

        for method_name in self.__dir__():
            if not method_name.startswith('filter_'):
                continue

            method = self.__getattribute__(method_name)
            if callable(method):
                method()

        return self.queryset

    def filter_tags(self) -> None:
        if self.params.tags:
            self.queryset = self.queryset.filter(**{self.filters.filter_field_tags: self.params.tags}).distinct()

    def filter_authors(self) -> None:
        if self.params.authors:
            self.queryset = self.queryset.filter(**{self.filters.filter_field_author: self.params.authors})

    def filter_years(self) -> None:
        if self.params.years and not self.params.years.is_default():
            self.queryset = self.queryset.filter(
                **{self.filters.filter_field_years_of_publication: (self.params.years.year_from, self.params.years.year_to)}
            )

    def filter_ordering(self) -> None:
        if self.params.ordering:
            self.queryset = self.queryset.order_by(self.params.ordering)
