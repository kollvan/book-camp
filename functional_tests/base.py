from functools import wraps
from typing import Callable

from django.contrib.auth import login
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.http import HttpRequest

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from goods.models import Category, Product, Author
from users.models import User


class FunctionalTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.browser, 10, 1)
        self.action = ActionChains(self.browser)

    def tearDown(self):
        self.browser.quit()

    def filled_db(self):
        self.author1 = Author.objects.create(name='Kit Tomson', slug='kit-tomson')
        self.author2 = Author.objects.create(name='Some Braun', slug='some-braun')
        self.category1 = Category.objects.create(name='Criptografy', slug='Cryptografy')
        self.category2 = Category.objects.create(name='Lessons', slug='lessons')
        self.product1 = Product.objects.create(name='CSS profi', slug='css-profi', description='Script Python all',
                                               author=self.author1, category=self.category1, quantity_page=2025)
        self.product2 = Product.objects.create(name='css profil', slug='css-profil', description='Script PYTHON',
                                               author=self.author2, category=self.category2, quantity_page=241)
    def create_user(self):
        self.username='test_user'
        self.password='234polnd'
        self.email='mypochta@damil.com'
        self.user = User.objects.create(username=self.username, email=self.email, password=self.password)
