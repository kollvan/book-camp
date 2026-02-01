from django.test import LiveServerTestCase, override_settings
from django.test.client import Client

from users.models import User


@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
})
class BaseInventoryTestCase(LiveServerTestCase):

    def setUp(self):
        self.full_live_server_url = f'{self.live_server_url}/inventory/collection/'
        self.client = Client()

    def create_and_login_user(self, username: str = 'kali', email: str = 'meandpochta@dmail.com'):
        self.user = User.objects.create_user(username=username, email=email, password='kalilinux')
        self.client.force_login(user=self.user)

    def tearDown(self):
        self.client.logout()
