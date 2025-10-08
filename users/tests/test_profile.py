import re

from django.db.models import Q
from django.utils.formats import date_format

from users.models import User
from users.tests.base import BaseUserTestCase, BaseWithoutUserTestCase


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

    def test_profile_default_image_content(self):
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

    def test_change_profile(self):
        data = {
            'username': 'changed_username',
            'first_name': 'changed_first_name',
            'last_name': 'changed_last_name',
            'email': 'changedemail@mail.com',
        }
        response = self.client.post(f'{self.live_server_url}/accounts/edit_profile/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(
                Q(username=data['username']) &
                Q(first_name=data['first_name']) &
                Q(last_name=data['last_name']) &
                Q(email=data['email'])
            ).exists()
        )


class TestUsersWithoutUser(BaseWithoutUserTestCase):

    def test_correct_register_user(self):
        data = {
            'username': 'test_user',
            'email': 'test_email@mail.com',
            'password1': '<:62N49ly,1)',
            'password2': '<:62N49ly,1)',
        }
        response = self.client.post(f'{self.live_server_url}/accounts/register/', data=data)
        self.assertRedirects(response, f'/accounts/login/')
        self.assertTrue(User.objects.filter(
            Q(username=data['username']) &
            Q(email=data['email'])
        ).exists()
                        )

    def test_login_page(self):
        response = self.client.get(f'{self.live_server_url}/accounts/login/')
        self.assertTemplateUsed(response, 'users/login.html')
        page_html = response.content.decode('utf-8')
        title = re.search(r'<title>(.*)</title>', page_html)
        self.assertEqual(title.group(1), 'Вход в акаунт')

    def test_login_page_content(self):
        response = self.client.get(f'{self.live_server_url}/accounts/login/')
        page_html = response.content.decode('utf-8')
        self.assertRegex(page_html, r'<input[^>]*name="username"[^>]*>')
        self.assertRegex(page_html, r'<input[^>]*name="password"[^>]*>')

    def test_register_page(self):
        response = self.client.get(f'{self.live_server_url}/accounts/register/')
        self.assertTemplateUsed(response, 'users/register.html')
        page_html = response.content.decode('utf-8')
        title = re.search(r'<title>(.*)</title>', page_html)
        self.assertEqual(title.group(1), 'Регистрация')

    def test_register_page_content(self):
        response = self.client.get(f'{self.live_server_url}/accounts/register/')
        page_html = response.content.decode('utf-8')
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2','image']
        for field in fields:
            self.assertRegex(page_html, rf'<input[^>]*name="{field}"[^>]*>')

    def test_successful_login_user(self):
        User.objects.create_user(username='test_user', email='emailuser@mail.com', password='password123')
        data = {
            'username': 'test_user',
            'password': 'password123',
        }
        response = self.client.post(f'{self.live_server_url}/accounts/login/', data=data)

        self.assertRedirects(response, '/')
        self.assertIn('sessionid', self.client.cookies)
