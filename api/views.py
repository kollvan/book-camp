from rest_framework import viewsets, filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api.filters_backends import IsOwnerFilterBackend, ExtendedSearchFilter, InventoryFilterBackend
from api.paginations import BaseAPIPagination
from api.permissions import IsStaffOrReadOnly
from api.serializers import CatalogSerializer, AuthorSerializer, CategorySerializer, TagsSerializer, \
    InventorySerializer, UserSerializer
from goods.models import Product, Author, Category, Tag
from inventory.models import Inventory
from users.models import User


# Create your views here.

class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = CatalogSerializer
    pagination_class = BaseAPIPagination
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (ExtendedSearchFilter, filters.OrderingFilter,)
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'quantity_page', 'year_of_publication']

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = BaseAPIPagination
    permission_classes = (IsStaffOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrReadOnly,)
    pagination_class = BaseAPIPagination

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = BaseAPIPagination
    permission_classes = (IsStaffOrReadOnly,)

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    pagination_class = BaseAPIPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (IsOwnerFilterBackend, InventoryFilterBackend,)


class UserAPIView(RetrieveUpdateDestroyAPIView):
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


