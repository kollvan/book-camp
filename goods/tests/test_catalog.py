import re

from goods.tests.base import BaseCatalogTestCase
from inventory.models import Inventory
from users.models import User


class TestCatalogWithoutAuthenticatedUser(BaseCatalogTestCase):

    def test_catalog_page(self):
        response = self.client.get(f'{self.full_live_server_url}/all/')
        self.assertTemplateUsed(response, 'goods/catalog.html')
        self.assertContains(response, '<title>BookCamp - Каталог</title>')

    def test_displayed_all_products(self):
        response = self.client.get(f'{self.full_live_server_url}/all/')
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_displayed_only_selected_category(self):
        response = self.client.get(f'{self.full_live_server_url}/{self.category1.slug}/')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_filter_by_tag(self):
        response = self.client.get(f'{self.full_live_server_url}/all/?tags={self.tag1.slug}')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_filter_by_author(self):
        response = self.client.get(f'{self.full_live_server_url}/all/?authors={self.author1.slug}')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_filter_by_year_of_publication(self):
        response = self.client.get(f'{self.full_live_server_url}/all/?year_from=2010&year_to=2019')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)




class TestCatalogWithAuthenticatedUser(BaseCatalogTestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='testuser', email='testuser@mail.com', password='password')
        self.client.force_login(self.user)

    def test_displayed_delete_button(self):
        Inventory.objects.create(user=self.user, product=self.product1)
        response = self.client.get(f'{self.full_live_server_url}/all/')
        html_page = response.content.decode('utf-8')
        regex = rf'<button[^>]*id\s*=\s*"?id_{self.product1.slug}-{self.product1.pk}"[^>]*>'
        button = re.search(regex, html_page)
        self.assertIn('remove', button.group(0))

    def test_displayed_add_button(self):
        response = self.client.get(f'{self.full_live_server_url}/all/')
        html_page = response.content.decode('utf-8')
        regex = rf'<button[^>]*id\s*=\s*"?id_{self.product1.slug}-{self.product1.pk}"[^>]*>'
        button = re.search(regex, html_page)
        self.assertNotIn('remove', button.group(0))

    def test_correct_avg_rank_displayed(self):
        tmp_user = User.objects.create(username='test', email='text@mail.com', password='password')
        Inventory.objects.create(user=self.user, rank=4, product=self.product1)
        Inventory.objects.create(user=tmp_user, rank=5, product=self.product1)
        response = self.client.get(self.full_live_server_url+'/all/')
        self.assertContains(response, 'Рейтинг: 4,5')
