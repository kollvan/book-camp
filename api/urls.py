from django.urls import path, include
from rest_framework import routers

from api.views import CatalogViewSet, AuthorViewSet, CategoryViewSet, TagsViewSet, InventoryViewSet, UserAPIView

router = routers.SimpleRouter()
router.register(r'catalog', CatalogViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'inventory', InventoryViewSet)

urlpatterns = [
    path('category/', CategoryViewSet.as_view({'get':'list', 'post':'create'})),
    path('tags/', TagsViewSet.as_view({'get':'list', 'post':'create'})),
    path('user/', UserAPIView.as_view()),
    path('', include(router.urls))
]