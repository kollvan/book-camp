from functools import wraps
from typing import Callable

from django import template
from django.core.cache import cache
from django.db.models import QuerySet
from django.template import Context
from django.utils.http import urlencode


def cache_custom_tag(cache_key: str, cache_time: int = 60) -> Callable:
    def func_decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> QuerySet:
            queryset = cache.get(f'{cache_key}_{'_'.join(args)}')
            if not queryset:
                queryset = func(*args, **kwargs)
                cache.set(f'{cache_key}_{'_'.join(args)}', queryset, cache_time)
            return queryset

        return wrapper

    return func_decorator
