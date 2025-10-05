import re

from django.utils.formats import date_format

from users.tests.base import BaseUserTestCase


class TestProfile(BaseUserTestCase):
    def test_profile_page(self):
        response = self.client.get(f'{self.live_server_url}/accounts/profile/')
        self.assertTemplateUsed(response, 'users/profile.html')
        html_page = response.content.decode('utf-8')
        title = re.search(r'<title>(.*)</title>', html_page)
        self.assertEqual(title.group(1), f'Bookcamp Profile - {self.user.username}')

    def test_profile_content(self):
        response = self.client.get(f'{self.live_server_url}/accounts/profile/')
        profile_fields = [self.user.last_name, self.user.email, self.user.first_name, self.user.username,
                          date_format(self.user.registration_date)]
        for field in profile_fields:
            self.assertContains(response, field)

    def test_profile_image_content(self):
        response = self.client.get(f'{self.live_server_url}/accounts/profile/')
        html_page = response.content.decode('utf-8')
        regex = r'<img[^>]*src="/static/bookcamp/image/default_profile_image.jpg"[^>]*>'
        self.assertRegex(html_page, regex)

    def test_change_profile_page(self):
        response = self.client.get(f'{self.live_server_url}/accounts/edit_profile/')
        self.assertTemplateUsed(response, 'users/edit_profile.html')
        html_page = response.content.decode('utf-8')
        title = re.search(r'<title>(.*)</title>', html_page)
        self.assertEqual(title.group(1), 'Редактировать профиль')

    def test_change_profile_content(self):
        response = self.client.get(f'{self.live_server_url}/accounts/edit_profile/')
        html_page = response.content.decode('utf-8')
        fields = ['image', 'username', 'email', 'first_name', 'last_name']
        for field in fields:
            self.assertRegex(html_page, rf'<input[^>]*name="{field}"[^>]*>')

