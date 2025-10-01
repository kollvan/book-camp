import re

from goods.models import Author, Category, Product, Tag
from inventory.models import Inventory
from inventory.tests.base import BaseInventoryTestCase
from users.models import User


class InventoryTestCase(BaseInventoryTestCase):
    def setUp(self):
        super().setUp()
        self.create_and_login_user()
        self.author1 = Author.objects.create(name='Kit grant', slug='kit-grant')
        self.category1 = Category.objects.create(name='cartoon', slug='cartoon')
        self.product1 = Product.objects.create(name='Python for all',
                                               slug='python-for-all',
                                               author=self.author1,
                                               category=self.category1,
                                               quantity_page=210, )
        self.author2 = Author.objects.create(name='Django fet', slug='django-fet')
        self.category2 = Category.objects.create(name='network', slug='network')
        self.product2 = Product.objects.create(name='Networks cookbook',
                                               slug='networks-cookbook',
                                               author=self.author2,
                                               category=self.category2,
                                               quantity_page=210, )

    def test_displayed_inventory_page(self):
        response = self.client.get(self.full_live_server_url)
        html_page = response.content.decode('utf-8')
        title = re.search(r'<title>(.*)</title>', html_page)
        self.assertEqual(title.group(1), f'Bookcamp Инвентарь - {self.user.username}')
        self.assertTemplateUsed(response, 'inventory/inventory.html')
        self.assertTemplateUsed(response, 'includes/pagination.html')

    def test_displayed_added_goods(self):
        Inventory.objects.create(user=self.user, product=self.product2)
        Inventory.objects.create(user=self.user, product=self.product1)

        response = self.client.get(self.full_live_server_url)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_displayed_category_dropdown_menu(self):
        response = self.client.get(self.full_live_server_url)
        html_page = response.content.decode('utf-8')
        self.assertRegex(html_page, fr'<option\s+value="{self.category1.slug}"')
        self.assertRegex(html_page, fr'<option\s+value="{self.category2.slug}"')

    def test_displayed_ordering_dropdown_menu(self):
        response = self.client.get(self.full_live_server_url)
        html_page = response.content.decode('utf-8')
        self.assertRegex(html_page, r'<option\s+value="')

    def test_user_dont_see_other_inventory(self):
        user2 = User.objects.create(username='user', email="other@mai.com", password='password')
        Inventory.objects.create(user=user2, product=self.product2)
        Inventory.objects.create(user=self.user, product=self.product1)

        response = self.client.get(self.full_live_server_url)
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)


class TestFilterInventory(BaseInventoryTestCase):
    def setUp(self):
        super().setUp()
        self.create_and_login_user()
        self.tag1 = Tag.objects.create(name='yaml', slug='yaml')
        self.author1 = Author.objects.create(name='Kit grant', slug='kit-grant')
        self.category1 = Category.objects.create(name='cartoon', slug='cartoon')
        self.product1 = Product.objects.create(name='Python for all',
                                               slug='python-for-all',
                                               author=self.author1,
                                               category=self.category1,
                                               quantity_page=210,
                                               year_of_publication=2020,
                                               )
        self.product1.tags.set([self.tag1, ])
        self.tag2 = Tag.objects.create(name='django', slug='django')
        self.author2 = Author.objects.create(name='Django fet', slug='django-fet')
        self.category2 = Category.objects.create(name='network', slug='network')
        self.product2 = Product.objects.create(name='Networks cookbook',
                                               slug='networks-cookbook',
                                               author=self.author2,
                                               category=self.category2,
                                               quantity_page=210,
                                               year_of_publication=2015,
                                               )
        self.product2.tags.set([self.tag2, ])
        Inventory.objects.create(user=self.user, status=3, product=self.product1)
        Inventory.objects.create(user=self.user, product=self.product2)

    def test_filtering_by_author(self):
        response = self.client.get(self.full_live_server_url + f'?authors={self.author1.slug}')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_filtering_by_year_of_publication(self):
        response = self.client.get(self.full_live_server_url + f'?year_from=2016&year_to=2021')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_filtering_by_tag(self):
        response = self.client.get(self.full_live_server_url + f'?tags={self.tag1.slug}')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_filtering_by_status(self):
        response = self.client.get(self.full_live_server_url + '?status=3')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_filtering_by_category(self):
        response = self.client.get(self.full_live_server_url + f'?category={self.category1.slug}')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)



class InventoryWithUnauthenticated(BaseInventoryTestCase):
    def test_open_page_inventory(self):
        response = self.client.get(self.full_live_server_url)
        self.assertEqual(response.status_code, 302)
        expected_url = '/accounts/login/?next=/inventory/collection/'
        self.assertRedirects(response, expected_url)
