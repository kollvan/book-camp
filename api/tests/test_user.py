from unittest import skip

from api.tests.base import BaseApiTestCase
from users.models import User

class EditUserTest(BaseApiTestCase):
    def setUp(self):
        super().setUp()
        self.live_server_url += 'user/'
        self.user.email = 'mymail@damil.com'

    def test_edit_other_user(self):
        fail_mail = 'myemail@dmail.com'
        User.objects.create_user(username='kali', password='1234', email='other_email@dmail.com')
        data = {
            'id':'2',
            'username':'kali',
            'password':'1456',
            'email': fail_mail,
        }
        response = self.client.patch(path=self.live_server_url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email=fail_mail))

    def test_edit_user(self):
        new_mail = 'newmail@dmail.com'
        data = {
            'email':new_mail
        }
        response = self.client.patch(path=self.live_server_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['email'])

