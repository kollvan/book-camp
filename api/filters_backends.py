import enum
import operator
from functools import reduce

from django.db import models
from rest_framework import filters


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)

class InventoryFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if cur_status := request.query_params.get('status'):
            return queryset.filter(status=cur_status)
        return queryset

class ExtendedSearchFilter(filters.SearchFilter):
    replace_fields={
            'authorName':'author__name',
            'authorSlug':'author__slug',
            'category':'category__name',
    }
    available_fields = {'name', 'description', 'authorName', 'authorSlug', 'category'}

    def _replace_fields(self, request_fields:list) -> list[str]:
        return [self.replace_fields.get(field, field) for field in request_fields]

    def get_search_fields(self, view, request):
        fields = []
        if params := request.query_params.get('search_fields'):
            fields = [param for param in params.split(',') if param in self.available_fields]
            fields = self._replace_fields(fields)

        if not fields:
             fields = super().get_search_fields(view,request)

        if request.query_params.get('strict'):
            fields = ['='+field for field in fields]
        return fields

