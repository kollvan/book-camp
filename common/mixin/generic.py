from django.core.cache import cache


class CacheViewMixin:
    cache_time = 60
    key_prefix = 'page'

    def get_object(self, queryset=None):
        slug = self.kwargs['product_slug']
        obj = cache.get(f'{self.key_prefix}_{slug}')
        if not obj:
            obj = super().get_object(queryset)
            cache.set(f'{self.key_prefix}_{slug}', obj, self.cache_time)
        return obj


class SelectRelatedMixin:
    related_fields = None
    prefetch_related_fields = None

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset\
            .select_related(*self.related_fields)\
            .prefetch_related(*self.prefetch_related_fields)
