from rest_framework import serializers
from slugify import slugify
from goods.models import Product, Author, Category, Tag
from inventory.models import Inventory
from users.models import User


class BaseSlugSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)
    def update(self, instance, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance=instance, validated_data=validated_data)

class CatalogSerializer(BaseSlugSerializer):
    set_category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    set_author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True)
    set_tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), write_only=True, many=True)
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1
    def create(self, validated_data):
        self._add_relation_fields(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._add_relation_fields(validated_data)
        return super().update(instance=instance, validated_data=validated_data)

    def _add_relation_fields(self, validated_data):
        validated_data['author'] = validated_data.pop('set_author')
        validated_data['category'] = validated_data.pop('set_category')
        validated_data['tags'] = validated_data.pop('set_tags')

class AuthorSerializer(BaseSlugSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(BaseSlugSerializer):
    class Meta:
        model=Category
        fields = '__all__'


class TagsSerializer(BaseSlugSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    set_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Inventory
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        validated_data['product'] = validated_data.pop('set_product')
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk','username','first_name', 'last_name', 'email', 'registration_date', 'image')
