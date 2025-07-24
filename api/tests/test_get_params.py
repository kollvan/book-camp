from unittest import skip

from api.tests.base import BaseApiTestCase
from goods.models import Author, Category, Product

class LatinSearchCatalogTest(BaseApiTestCase):
    def setUp(self):
        author1 = Author.objects.create(name='Kit Tomson', slug='kit-tomson')
        author2 = Author.objects.create(name='Some Braun', slug='some-braun')
        category1 = Category.objects.create(name='Criptografy', slug='Cryptografy')
        category2 = Category.objects.create(name='Lessons', slug='lessons')
        self.product1 = Product.objects.create(name='CSS profi', description='description Python',
                                               author=author1, category=category1, quantity_page=2025)
        self.product2 = Product.objects.create(name='Python all', description='description css',
                                               author=author2, category=category2, quantity_page=241)
        super().setUp()
        self.live_server_url += 'catalog/'

    def test_search_by_name(self):
        search_text = 'cS'
        response = self.client.get(path=self.live_server_url + f'?search={search_text}&search_fields=name')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_search_by_description(self):
        search_text = 'THon'
        response = self.client.get(path=self.live_server_url + f'?search={search_text}&search_fields=description')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_search_by_author_name(self):
        search_text = 'some'
        response = self.client.get(path=self.live_server_url + f'?search={search_text}&search_fields=authorName')
        self.assertContains(response, self.product2.name)
        self.assertNotContains(response, self.product1.name)

    def test_search_by_category_name(self):
        search_text = 'cript'
        response = self.client.get(path=self.live_server_url + f'?search={search_text}&search_fields=category')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)


class LatinWithStrictSearchCatalogTest(BaseApiTestCase):
    def setUp(self):
        author1 = Author.objects.create(name='Kit Tomson', slug='kit-tomson')
        author2 = Author.objects.create(name='Some Braun', slug='some-braun')
        category1 = Category.objects.create(name='Criptografy', slug='Cryptografy')
        category2 = Category.objects.create(name='Lessons', slug='lessons')
        self.product1 = Product.objects.create(name='CSS profi', description='Script Python all',
                                               author=author1, category=category1, quantity_page=2025)
        self.product2 = Product.objects.create(name='css profil', description='Script PYTHON',
                                               author=author2, category=category2, quantity_page=241)
        super().setUp()
        self.live_server_url += 'catalog/'

    def test_search_by_name(self):
        search_text = "'CSS profi'"
        response = self.client.get(path=self.live_server_url + f'?search={search_text}&search_fields=name&strict=1')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_search_by_description(self):
        search_text = '"Script PYTHON"'
        response = self.client.get(
            path=self.live_server_url + f'?search={search_text}&search_fields=description&strict=1'
        )
        self.assertContains(response, self.product2.name)
        self.assertNotContains(response, self.product1.name)

class CyrillicSearchCatalogTest(BaseApiTestCase):
    def setUp(self):
        author1 = Author.objects.create(name='Кит Том Сон', slug='kit-tom-son')
        author2 = Author.objects.create(name='Сом Браунт', slug='some-braun')
        category1 = Category.objects.create(name='Криптография', slug='criptography')
        category2 = Category.objects.create(name='Занятия', slug='zaniatia')
        self.product1 = Product.objects.create(name='Для профильного', description='Другой положение',
                                               author=author1, category=category1, quantity_page=2025)
        self.product2 = Product.objects.create(name='Положение звёзд', description='Профильное описание',
                                               author=author2, category=category2, quantity_page=241)
        super().setUp()
        self.live_server_url += 'catalog/'

    def test_search_by_author_name(self):
        search_text = 'Том с'
        response = self.client.get(path=self.live_server_url + f'?search={search_text}&search_fields=authorName')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_search_by_name(self):
        search_text = 'я Проф'
        response = self.client.get(path=self.live_server_url + f'?search={search_text}&search_fields=name')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)
    def test_search_by_descirption(self):
        search_text = 'Ание'
        response = self.client.get(path=self.live_server_url + f'?search={search_text}&search_fields=description')
        self.assertContains(response, self.product2.name)
        self.assertNotContains(response, self.product1.name)

    def test_search_by_category_name(self):
        search_text = 'тия'
        response = self.client.get(path=self.live_server_url + f'?search={search_text}&search_fields=category')
        self.assertContains(response, self.product2.name)
        self.assertNotContains(response, self.product1.name)