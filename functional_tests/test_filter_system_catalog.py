from functional_tests.base import FunctionalTestCase
from goods.models import Author, Tag, Product, Category

from selenium.webdriver.support import expected_conditions as EC


class TestFilterSystemPageCatalog(FunctionalTestCase):
    def setUp(self):
        super().setUp()
        self.filled_db()
        self.browser.set_window_size(1920, 1080)

    def filled_db(self):
        self.category = Category.objects.create(name='test', slug='test')
        self.author1 = Author.objects.create(name='kit grant', slug='kit-grant')
        self.author2 = Author.objects.create(name='john johnson', slug='john-johnson')
        self.tag1 = Tag.objects.create(name='html', slug='html')
        self.tag2 = Tag.objects.create(name='css', slug='css')
        self.year1 = 2002
        self.year2 = 2022
        self.product1 = Product.objects.create(
            name='MyHTML', slug='myhtml', author=self.author1,
            quantity_page=204, category=self.category, year_of_publication=self.year1
        )
        self.product1.tags.set([self.tag1, ])
        self.product2 = Product.objects.create(
            name='OtherHTML', slug='otherhtml', author=self.author2,
            quantity_page=204, category=self.category, year_of_publication=self.year1
        )
        self.product2.tags.set([self.tag1, ])
        self.product3 = Product.objects.create(
            name='MyCSS', slug='mycss', author=self.author1,
            quantity_page=204, category=self.category, year_of_publication=self.year1
        )
        self.product3.tags.set([self.tag2, ])
        self.product4 = Product.objects.create(
            name='OldHTML', slug='oldhtml', author=self.author1,
            quantity_page=204, category=self.category, year_of_publication=self.year2
        )
        self.product4.tags.set([self.tag1, ])

    def test_filters_year_author_tag_for_catalog(self):
        PRODUCT_HTML_LOCATOR = ('xpath', f'//div[@id="id_{self.product1.slug}"]')
        PRODUCT_OTHER_HTML_LOCATOR = ('xpath', f'//div[@id="id_{self.product2.slug}"]')
        PRODUCT_CSS_LOCATOR = ('xpath', f'//div[@id="id_{self.product3.slug}"]')
        PRODUCT_OLD_HTML_LOCATOR = ('xpath', f'//div[@id="id_{self.product4.slug}"]')

        BUTTON_SUBMIT_LOCATOR = ('xpath', '//button[@id="filter-submit"]')
        TAG_LABEL_LOCATOR = ('xpath', f'//label[@for="id_{self.tag1.slug}"]')
        AUTHOR_LABEL_LOCATOR = ('xpath', f'//label[@for="id_{self.author1.slug}"]')
        YEAR_BUTTON_LOCATOR = ('xpath', f'//button[@id="button-to-down"]')

        self.browser.get(f'{self.live_server_url}/books/catalog/{self.category.slug}/')

        self.wait.until(EC.element_to_be_clickable(TAG_LABEL_LOCATOR)).click()

        self.wait.until(EC.element_to_be_clickable(BUTTON_SUBMIT_LOCATOR)).click()

        self.wait.until(EC.url_contains(f'tags={self.tag1.slug}'))
        self.wait.until(EC.visibility_of_element_located(PRODUCT_HTML_LOCATOR))
        self.wait.until(EC.visibility_of_element_located(PRODUCT_OTHER_HTML_LOCATOR))
        self.wait.until(EC.visibility_of_element_located(PRODUCT_OLD_HTML_LOCATOR))
        assert not self.browser.find_elements(*PRODUCT_CSS_LOCATOR), 'Error filtering by tag.'

        self.wait.until(EC.element_to_be_clickable(AUTHOR_LABEL_LOCATOR)).click()

        self.wait.until(EC.element_to_be_clickable(BUTTON_SUBMIT_LOCATOR)).click()

        self.wait.until(EC.url_contains(f'authors={self.author1.slug}'))
        self.wait.until(EC.visibility_of_element_located(PRODUCT_HTML_LOCATOR))
        self.wait.until(EC.visibility_of_element_located(PRODUCT_OLD_HTML_LOCATOR))
        assert not self.browser.find_elements(*PRODUCT_OTHER_HTML_LOCATOR), 'Error filtering by author.'

        year_button = self.wait.until(EC.element_to_be_clickable(YEAR_BUTTON_LOCATOR))
        for _ in range(5):
            year_button.click()

        self.wait.until(EC.element_to_be_clickable(BUTTON_SUBMIT_LOCATOR)).click()

        self.wait.until(EC.url_contains('year_to=2020'))
        self.wait.until(EC.visibility_of_element_located(PRODUCT_HTML_LOCATOR))
        assert not self.browser.find_elements(*PRODUCT_OLD_HTML_LOCATOR), 'Error filtering by year.'
