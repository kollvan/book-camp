from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple, List

from django.contrib.postgres.search import SearchVector, SearchHeadline, SearchQuery, SearchRank
from django.db.models import QuerySet, Avg

from goods.models import Product


def get_current_year() -> str:
    return str(datetime.now().year)


class RangeYear(NamedTuple):
    year_from: str = '0'
    year_to: str = get_current_year()

    def is_default(self) -> bool:
        return self.year_from == '0' and self.year_to == get_current_year()


def search(query: str, expressions: List[str]) -> QuerySet:
    search_vector = SearchVector(*expressions)
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
    is_high_rank: bool = None


@dataclass
class Filters:
    filter_field_tags: str = 'tags__slug__in'
    filter_field_authors: str = 'author__slug__in'
    filter_field_years_of_publication: str = 'year_of_publication__range'
    filter_field_high_rank: str = 'inventory__rank'


class FilterQueryset:
    def __init__(self, queryset: QuerySet):
        self.queryset = queryset

    def get_filter_queryset(self, params: FilterParams, filters: Filters = Filters()) -> QuerySet:
        params_data = params.__dict__
        filters_data = filters.__dict__

        for method_name in self.__dir__():
            if not method_name.startswith('filter_'):
                continue

            method = self.__getattribute__(method_name)
            if callable(method):
                method(**params_data, **filters_data)

        return self.queryset.distinct()

    def filter_tags(self, tags, filter_field_tags, **kwargs) -> None:
        if tags:
            self.queryset = self.queryset.filter(**{filter_field_tags: tags})

    def filter_authors(self, authors, filter_field_authors, **kwargs) -> None:
        if authors:
            self.queryset = self.queryset.filter(**{filter_field_authors: authors})

    def filter_years(self, years, filter_field_years_of_publication, **kwargs) -> None:
        if years and not years.is_default():
            self.queryset = self.queryset.filter(
                **{filter_field_years_of_publication: (years.year_from, years.year_to)}
            )

    def filter_ordering(self, ordering, **kwargs) -> None:
        if ordering:
            self.queryset = self.queryset.order_by(ordering)

    def filter_is_high_rank(self, is_high_rank, filter_field_high_rank, **kwargs) -> None:
        if is_high_rank:
            self.queryset = (self.queryset
                             .filter(**{f'{filter_field_high_rank}__gt':0})
                             .annotate(avg_rating=Avg(filter_field_high_rank))
                             .filter(avg_rating__gte=4))

