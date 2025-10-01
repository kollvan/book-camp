from django.test import LiveServerTestCase
from django.test.client import Client

from goods.models import Tag, Author, Category, Product


class BaseProductTestCase(LiveServerTestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name='django', slug='django')
        self.author = Author.objects.create(name='Django fet', slug='django-fet')
        self.category = Category.objects.create(name='network', slug='network')
        self.product = Product.objects.create(name='Networks cookbook',
                                               slug='networks-cookbook',
                                               author=self.author,
                                               category=self.category,
                                               quantity_page=210,
                                               year_of_publication=2015,
                                               )
        self.product.tags.set([self.tag, ])
        self.client = Client()
        self.full_live_server_url = f'{self.live_server_url}/books/product/{self.product.slug}/'
    def tearDown(self):
        self.client.logout()

