from django.test import LiveServerTestCase
from django.test.client import Client

from users.models import User


class BaseInventoryTestCase(LiveServerTestCase):

    def setUp(self):
        self.live_server_url = 'http://127.0.0.1:8000/inventory/collection/'
        self.client = Client()

    def create_and_login_user(self, username: str = 'kali', email: str = 'meandpochta@dmail.com'):
        self.user = User.objects.create_user(username=username, email=email, password='kalilinux')
        self.client.force_login(user=self.user)

    def tearDown(self):
        self.client.logout()
