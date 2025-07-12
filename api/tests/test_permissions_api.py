from unittest import skip

from django.core.paginator import UnorderedObjectListWarning
from django.test import LiveServerTestCase
from rest_framework.test import APIClient

from goods.models import Author, Product, Category, Tag
from inventory.models import Inventory
from users.models import User

import warnings
warnings.filterwarnings("ignore", category=UnorderedObjectListWarning)

class GETUserExistsNotStaffTest(LiveServerTestCase):
    '''TestCase with GET request for user who is not staff'''
    def setUp(self):
        self.author = Author.objects.create(name='author1', slug='author1')
        self.category = Category.objects.create(name='category1', slug='category1')
        self.tag = Tag.objects.create(name='tag1', slug='tag1')
        self.product = Product.objects.create(name='product1', author=self.author, quantity_page=10, category=self.category)
        self.product.tags.add(self.tag)
        self.user = User.objects.create_user(username='nikem', password='kalilinux')
        self.live_server_url = 'http://localhost:8000/api/'
        self.client = APIClient()
        self.client.login(username='nikem', password='kalilinux')

    def tearDown(self):
        self.client.logout()

    def test_get_user(self):
        '''Test to get your user data'''
        response = self.client.get(self.live_server_url + 'user/')
        self.assertContains(response, 'nikem')
    def test_get_only_self_user(self):
        '''Test to get only your user data'''
        User.objects.create_user(username='other_user', password='123')
        response = self.client.get(self.live_server_url + 'user/')
        self.assertNotContains(response, 'other_user')
    def test_get_tag(self):
        '''Test to get model Tag data'''
        response = self.client.get(self.live_server_url + 'tags/')
        self.assertContains(response, 'tag1')
    def test_get_authors(self):
        '''Test to get model Author data'''
        response = self.client.get(self.live_server_url + 'authors/')
        self.assertContains(response, 'author1')

    def test_get_category(self):
        '''Test to get model Author data'''
        response = self.client.get(self.live_server_url + 'category/')
        self.assertContains(response, 'category1')
    def test_get_inventory(self):
        '''Test to get model Inventory data'''
        Inventory.objects.create(product=self.product, user=self.user)
        response = self.client.get(path=self.live_server_url + 'inventory/')
        self.assertContains(response, 'product1')
    def test_get_only_self_inventory(self):
        Inventory.objects.create(product=self.product, user=self.user)
        other_user = User.objects.create_user(username='user2', password='1234')
        other_product = Product.objects.create(name='other_product',
                                               author=self.author, quantity_page=10, category=self.category)
        Inventory.objects.create(product=other_product, user=other_user)
        response = self.client.get(path=self.live_server_url + 'inventory/')
        self.assertNotContains(response, 'other_product')

class POSTUserExistsNotStaffTest(LiveServerTestCase):
    '''TestCase with POST request for user who is not staff'''

    def setUp(self):
        self.live_server_url = 'http://localhost:8000/api/'
        self.user = User.objects.create_user(username='nikem', password='kalilinux')
        self.client = APIClient()
        self.client.login(username='nikem', password='kalilinux')

    def tearDown(self):
        self.client.logout()
    def test_add_authors(self):
        '''Test add new author'''
        data = {'name':'author1'}
        response = self.client.post(path=self.live_server_url + 'authors/', data=data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Author.objects.all())
    def test_add_category(self):
        '''Test add new category'''
        data = {'name':'category1'}
        response = self.client.post(path=self.live_server_url + 'category/', data=data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Category.objects.all())


    def test_add_tag(self):
        '''Test add new tag'''
        data = {'name': 'tag1'}
        response = self.client.post(path=self.live_server_url + 'tags/', data=data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Tag.objects.all())


    def test_add_product(self):
        '''Test add new product'''
        author = Author.objects.create(name='author1', slug='author1')
        category = Category.objects.create(name='category1', slug='category1')
        data = {
            'name':'product1',
            'set_author': author.pk,
            'quantity_page':10,
            'set_category': category.pk,
        }
        response = self.client.post(path=self.live_server_url + 'catalog/',data=data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Product.objects.all())

    def test_add_inventory(self):
        '''Test add new record in Inventory model for current user'''
        author = Author.objects.create(name='author1', slug='author1')
        category = Category.objects.create(name='category1', slug='category1')
        product = Product.objects.create(name='product1', author=author, quantity_page=10,
                                              category=category)
        data = {
            'set_product': product.pk,
            'user': self.user.pk
        }
        response = self.client.post(path=self.live_server_url + 'inventory/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Inventory.objects.filter(user=self.user, product=product.pk))
    def test_add_inventory_only_self(self):
        '''Test add new record in Inventory model for other user'''
        author = Author.objects.create(name='author1', slug='author1')
        category = Category.objects.create(name='category1', slug='category1')
        product = Product.objects.create(name='product1', author=author, quantity_page=10,
                                              category=category)
        user = User.objects.create_user(username='other_user', password='1234')
        data = {
            'set_product': product.pk,
            'user': user.pk
        }
        self.client.post(path=self.live_server_url + 'inventory/', data=data)
        self.assertFalse(Inventory.objects.filter(user=user, product=product.pk))


class PostUserExistsStaffTest(LiveServerTestCase):
    def setUp(self):
        self.live_server_url = 'http://localhost:8000/api/'
        self.user = User.objects.create_user(username='nikem', password='kalilinux', is_staff=True)
        self.client = APIClient()
        self.client.login(username='nikem', password='kalilinux')

    def tearDown(self):
        self.client.logout()

    def test_add_author(self):
        data = {
            'name':'author1'
        }
        response = self.client.post(path=self.live_server_url + 'authors/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Author.objects.filter(name=data['name']))

    def test_add_category(self):
        data = {
            'name':'category1'
        }
        response = self.client.post(path=self.live_server_url + 'category/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Category.objects.filter(name=data['name']))

    def test_add_tag(self):
        data = {
            'name':'tag1'
        }
        response = self.client.post(path=self.live_server_url + 'tags/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Tag.objects.filter(name=data['name']))

    def test_add_product(self):
        author = Author.objects.create(name='author1', slug='author1')
        category = Category.objects.create(name='category1', slug='category1')
        data = {
            'name':'product1',
            'set_author': author.pk,
            'set_category': category.pk,
            'quantity_page':100,
        }
        response = self.client.post(path=self.live_server_url + 'catalog/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name=data['name']))