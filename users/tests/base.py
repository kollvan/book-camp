from django.test import LiveServerTestCase
from django.test.client import Client

from users.models import User


class BaseUserTestCase(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            first_name='myprofile',
            last_name='bakery',
            email='tests@mail.com',
            password='password')
        self.client = Client()
        self.client.force_login(self.user)

    def tearDown(self):
        self.client.logout()

class BaseWithoutUserTestCase(LiveServerTestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        self.client.logout()