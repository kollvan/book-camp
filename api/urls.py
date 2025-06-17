from django.urls import path

from api.views import CatalogViewSet, AuthorViewSet, CategoryViewSet, TagsViewSet, InventoryViewSet

urlpatterns = [
    path('catalog/', CatalogViewSet.as_view({'get':'list', 'post':'create'})),
    path('catalog/<int:pk>/', CatalogViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('authors/', AuthorViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('authors/<int:pk>/', AuthorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('category/', CategoryViewSet.as_view({'get':'list', 'post':'create'})),
    path('tags/', TagsViewSet.as_view({'get':'list', 'post':'create'})),
    path('inventory/', InventoryViewSet.as_view({'get':'list', 'post':'create'})),
    path('inventory/<int:pk>/', InventoryViewSet.as_view({'put':'update', 'delete':'destroy'})),
]