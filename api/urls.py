from django.urls import path, include, re_path
from rest_framework import routers

from api.views import CatalogViewSet, AuthorViewSet, CategoryViewSet, TagsViewSet, InventoryViewSet, UserAPIView

router = routers.SimpleRouter()
router.register(r'catalog', CatalogViewSet)
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    path('category/', CategoryViewSet.as_view({'get':'list', 'post':'create'})),
    path('tags/', TagsViewSet.as_view({'get':'list', 'post':'create'})),
    path('inventory/', InventoryViewSet.as_view({'get':'list', 'post':'create'})),
    path('inventory/<slug:product_slug>/', InventoryViewSet.as_view({'delete':'destroy', 'patch':'partial_update'})),
    path('user/', UserAPIView.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]