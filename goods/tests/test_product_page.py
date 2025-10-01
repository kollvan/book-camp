import re

from goods.tests.base import BaseProductTestCase
from inventory.models import Inventory
from users.models import User


class TestProductTestCase(BaseProductTestCase):

    def test_displayed_inventory_page(self):
        """Checking the use of required templates and the correctness of the title."""
        response = self.client.get(self.full_live_server_url)
        html_page = response.content.decode('utf-8')
        title = re.search(r'<title>(.*)</title>', html_page)
        self.assertEqual(title.group(1), self.product.name)
        self.assertTemplateUsed(response, 'goods/product.html')

    def test_display_avg_rank(self):
        """Сhecking the display of the correct rating."""
        user = User.objects.create(username="test", email='test@email.com', password='password12')
        user1 = User.objects.create(username="test1", email='test1@email.com', password='password12')
        Inventory.objects.create(user=user, rank=5, product=self.product)
        Inventory.objects.create(user=user1,rank=4, product=self.product)

        response = self.client.get(self.full_live_server_url)
        page_html = response.content.decode('utf-8')
        self.assertRegex(page_html, r'\s?Рейтинг:\s+4,5\s?')
