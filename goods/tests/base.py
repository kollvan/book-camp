from typing import List, NamedTuple, Dict, Any

from django.test import LiveServerTestCase, override_settings
from django.test.client import Client

from goods.models import Tag, Author, Category, Product
from inventory.models import Inventory
from users.models import User


@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
})
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


class UserInventory(NamedTuple):
    product: Product
    rank: int | None = None
    review: str | None = None
    status: int | None = None

    def get_data(self) -> Dict['str', Any]:
        return {key: value for key, value in self._asdict().items() if value is not None}


class BaseCatalogTestCase(LiveServerTestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name='django', slug='django')
        self.author1 = Author.objects.create(name='Django fet', slug='django-fet')
        self.category1 = Category.objects.create(name='network', slug='network')
        self.product1 = Product.objects.create(name='Networks cookbook',
                                               slug='networks-cookbook',
                                               author=self.author1,
                                               category=self.category1,
                                               quantity_page=210,
                                               year_of_publication=2015,
                                               )

        self.product1.tags.set([self.tag1, ])
        self.tag2 = Tag.objects.create(name='celery', slug='celery')
        self.author2 = Author.objects.create(name='Dambldor', slug='dambldor')
        self.category2 = Category.objects.create(name='session', slug='session')
        self.product2 = Product.objects.create(name='Session key',
                                               slug='session-key',
                                               author=self.author2,
                                               category=self.category2,
                                               quantity_page=210,
                                               year_of_publication=2020,
                                               )
        self.product2.tags.set([self.tag2, ])
        self.full_live_server_url = f'{self.live_server_url}/books/catalog'
        self.client = Client()

    def fill_inventory(
            self,
            usernames: List[str],
            inventory_data: List[List[UserInventory]] | None = None,
    ) -> Dict['str', User]:
        users = {}
        for idx, username in enumerate(usernames):
            if username in users:
                continue

            users[username] = User.objects.create(
                username=username,
                email=f'{username}@email.com',
                password='1234',
            )
            if inventory_data and len(inventory_data) > idx:
                for record in inventory_data[idx]:
                    Inventory.objects.create(
                        user=users[username],
                        **record.get_data()
                    )
        return users
