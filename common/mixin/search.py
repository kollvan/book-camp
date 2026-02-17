from typing import Dict

from django.contrib.postgres.search import SearchRank, SearchVector, SearchQuery, SearchHeadline
from django.db.models import QuerySet


class SearchMixin:
    search_fields: Dict[str, str] = None

    def search(self, query: str) -> QuerySet:
        search_vector = SearchVector(*self.search_fields.values())
        query = SearchQuery(query)
        records = self.model.objects.annotate(
            search_rank=SearchRank(search_vector, query)
        ).filter(search_rank__gt=0).order_by('-search_rank')

        headlines = {}
        for key, field_name in self.search_fields.items():
            headline = SearchHeadline(field_name, query, start_sel='<span class="select">', stop_sel='</span>')
            headlines[f'headline_{key}'] = headline

        return records.annotate(**headlines)
