from rest_framework import viewsets, filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api.filters_backends import IsOwnerFilterBackend
from api.paginations import CatalogPagination
from api.permissions import IsAdminOrReadOnly
from api.serializers import CatalogSerializer, AuthorSerializer, CategorySerializer, TagsSerializer, \
    InventorySerializer, UserSerializer
from goods.models import Product, Author, Category, Tag
from inventory.models import Inventory
from users.models import User


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

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    pagination_class = CatalogPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (IsOwnerFilterBackend,)


class UserAPIView(RetrieveUpdateDestroyAPIView):
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


