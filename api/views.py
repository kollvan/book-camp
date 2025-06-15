from rest_framework import viewsets

from api.paginations import CatalogPagination
from api.permissions import IsAdminOrReadOnly
from api.serializers import CatalogSerializer, AuthorSerializer, CategorySerializer, TagsSerializer
from goods.models import Product, Author, Category, Tag


# Create your views here.

class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = CatalogSerializer
    pagination_class = CatalogPagination
    permission_classes = (IsAdminOrReadOnly,)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = CatalogPagination
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CatalogPagination

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = CatalogPagination
    permission_classes = (IsAdminOrReadOnly,)



