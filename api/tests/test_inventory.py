from django.core.paginator import UnorderedObjectListWarning

from api.tests.base import BaseApiTestCase
from goods.models import Author, Category, Product
from inventory.models import Inventory

import warnings
warnings.filterwarnings("ignore", category=UnorderedObjectListWarning)
class InventoryTest(BaseApiTestCase):
    def setUp(self):
        super().setUp()

        author = Author.objects.create(name='Some Braun', slug='some-braun')
        category = Category.objects.create(name='Lessons', slug='lessons')
        self.product = Product.objects.create(name='CSS profi', slug='css-profi', description='Script Python all',
                                               author=author, category=category, quantity_page=2025)
        self.inventory = Inventory.objects.create(user=self.user, product=self.product)

    def test_delete_inventory(self):
        response = self.client.delete(path=self.live_server_url+f'inventory/{self.product.slug}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Inventory.objects.filter(user=self.user.pk, product=self.product))

    def test_get_list_inventory(self):
        product2 = Product.objects.create(name='html dla profi', slug='html-dla-profi',
                               author=self.product.author, category=self.product.category,quantity_page=256)
        Inventory.objects.create(user=self.user, product=product2)
        response = self.client.get(path=self.live_server_url + 'inventory/')
        self.assertContains(response, self.product.slug)
        self.assertContains(response, product2.slug)
    def test_patch_inventory(self):
        data = {
            'rank':'3.56',
        }
        response = self.client.patch(path=self.live_server_url + f'inventory/{self.product.slug}/', data=data)
        self.assertContains(response, f'"rank":"{data['rank']}"')

    def test_patch_inventory_for_status(self):
        data={
            'status' : '3',
        }
        response = self.client.patch(path=self.live_server_url + f'inventory/{self.product.slug}/', data=data)
        self.assertContains(response, f'"status":"{data['status']}"')
