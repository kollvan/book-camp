from goods.tests.base import BaseProductTestCase
from inventory.models import Inventory
from users.models import User


class TestReviewsPagination(BaseProductTestCase):
    def setUp(self):
        super().setUp()
        self.user_profiles = [f'user{i}' for i in range(6)]
        for username in self.user_profiles:
            user = User.objects.create(username=username, email=f'{username}@gmail.com', password=username)
            Inventory.objects.create(user=user, product=self.product, review=f'I`m {username}')

    def test_displayed_reviews_on_page_product(self):
        response = self.client.get(self.full_live_server_url)
        self.assertContains(response, self.user_profiles[0])
        self.assertContains(response, self.user_profiles[1])
        self.assertContains(response, 'id="link-show-more"')

    def test_getting_reviews_from_API(self):
        page = 2
        page_size = 2
        url = f'/inventory/widgets/reviews/{self.product.slug}/'
        response = self.client.get(f'{self.live_server_url}{url}?page={page}')
        data = response.json()
        self.assertEqual(data['next'],  f'{url}?page={page + 1}')
        for username in self.user_profiles[page_size*(page-1): page_size]:
            self.assertIn(username, data['reviews'])
            self.assertIn(f'I`m {username}', data['reviews'])

    def test_getting_last_reviews_from_API(self):
        page = 3
        page_size = 2
        url = f'/inventory/widgets/reviews/{self.product.slug}/'
        response = self.client.get(f'{self.live_server_url}{url}?page={page}')
        data = response.json()
        self.assertFalse(data['next'])
        for username in self.user_profiles[page_size*(page-1): page_size]:
            self.assertIn(username, data['reviews'])
            self.assertIn(f'I`m {username}', data['reviews'])

    def test_getting_not_exists_reviews_from_API(self):
        page = 4
        url = f'/inventory/widgets/reviews/{self.product.slug}/'
        response = self.client.get(f'{self.live_server_url}{url}?page={page}')
        data = response.json()
        self.assertFalse(data['next'])
        self.assertFalse(data['reviews'])