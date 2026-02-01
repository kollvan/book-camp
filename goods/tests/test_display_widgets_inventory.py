from goods.tests.base import BaseProductTestCase
from inventory.models import Inventory
from users.models import User


class TestDisplayUserDataWithAddedGood(BaseProductTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='test', email='test@mail.com', password='password23')
        Inventory.objects.create(user=self.user, product=self.product)
        self.client.force_login(self.user)

    def test_displayed_user_data(self):
        """Checking the use of the user_data template(widget) when adding good."""
        response = self.client.get(self.full_live_server_url)
        self.assertTemplateUsed(response, 'includes/user_data_product.html')
        self.assertTemplateUsed(response, 'includes/user_review.html')



class TestDisplayUserDataWithoutAuthenticated(BaseProductTestCase):

    def test_not_displayed_user_data(self):
        """Checking for non-use of the user_data template(widget) when don`t adding good."""
        response = self.client.get(self.full_live_server_url)
        self.assertTemplateNotUsed(response, 'includes/user_data_product.html')
