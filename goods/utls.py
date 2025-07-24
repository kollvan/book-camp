from datetime import datetime
from typing import NamedTuple

from django.contrib.postgres.search import SearchVector, SearchHeadline, SearchQuery, SearchRank

from goods.models import Product


def get_current_year() -> str:
    return str(datetime.now().year)

class RangeYear(NamedTuple):
    year_from:str = '0'
    year_to:str = '2025'

    def is_default(self):
        return self.year_from =='0' and self.year_to == get_current_year()

def search(query):
    search_vector = SearchVector('name', 'description')
    query=SearchQuery(query)
    records = Product.objects.annotate(rank=SearchRank(search_vector, query)).filter(rank__gt=0).order_by('-rank')

    records = records.annotate(headline=SearchHeadline('name', query,
                                             start_sel='<span class="select">',
                                             stop_sel='</span>'))
    records = records.annotate(bodyline=SearchHeadline('description', query,
                                             start_sel='<span class="select">',
                                             stop_sel='</span>'))
    return records
