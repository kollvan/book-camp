from django.test import LiveServerTestCase
from rest_framework.test import APIClient

from users.models import User


class BaseApiTestCase(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='nikem', password='kalilinux')
        self.live_server_url = 'http://localhost:8000/api/'
        self.client = APIClient()
        self.client.login(username='nikem', password='kalilinux')

    def tearDown(self):
        self.client.logout()