from goods.models import Author, Category, Product
from inventory.models import Inventory
from inventory.tests.base import BaseInventoryTestCase


class TestUserData(BaseInventoryTestCase):

    def setUp(self):
        super().setUp()
        super().create_and_login_user()
        self.live_server_url = 'http://127.0.0.1:8000/books/product'
        self.author = Author.objects.create(name='Kit grant', slug='kit-grant')
        self.category = Category.objects.create(name='cartoon', slug='cartoon')
        self.product = Product.objects.create(name='Python for all',
                                              slug='python-for-all',
                                              author=self.author,
                                              category=self.category,
                                              quantity_page=210, )

    def test_displayed_user_data(self):
        """Display user_data if the user added the current product."""
        Inventory.objects.create(user=self.user, product=self.product)
        response = self.client.get(f'{self.live_server_url}/{self.product.slug}/')
        self.assertContains(response, 'class="user-data"')

    def test_not_displayed_user_data(self):
        """user_data is not displayed if the user hasn`t added the current product."""
        response = self.client.get(f'{self.live_server_url}/{self.product.slug}/')
        self.assertNotContains(response, 'class="user-data"')

    def test_displayed_add_button(self):
        """Displayed button add for unadded good in inventory."""
        response = self.client.get(f'{self.live_server_url}/{self.product.slug}/')
        self.assertContains(response, 'btn-add')

    def test_not_displayed_add_button(self):
        """Don't displayed button add for added good in inventory."""
        Inventory.objects.create(user=self.user, product=self.product)
        response = self.client.get(f'{self.live_server_url}/{self.product.slug}/')
        self.assertNotContains(response, 'btn-add')

    def test_getting_user_data(self):
        """Check received user_data."""
        Inventory.objects.create(user=self.user, product=self.product)
        response = self.client.get(f'http://127.0.0.1:8000/inventory/widgets/user_data/{self.product.slug}/')

        user_data = response.json()['user_data']
        self.assertEqual(response.status_code, 200)
        self.assertIn('name="product_status"', user_data)
        self.assertIn('name="product_rank"', user_data)
        self.assertIn('btn-remove', user_data)

    def test_getting_user_data_with_error_404(self):
        """Check received user_data for incorrect good slug."""
        response = self.client.get('http://127.0.0.1:8000/inventory/widgets/user_data/other_product/')
        self.assertEqual(response.status_code, 404)


class TestUserDataWithUserNotAuthenticated(BaseInventoryTestCase):
    def test_getting_user_data_with_error_403(self):
        """Check received user_data for unauthenticated user."""
        response = self.client.get('http://127.0.0.1:8000/inventory/widgets/user_data/other_product/')
        self.assertEqual(response.status_code, 403)
