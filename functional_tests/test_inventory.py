from django.middleware.csrf import _get_new_csrf_string
from selenium.webdriver.support.select import Select

from functional_tests.base import FunctionalTestCase
from selenium.webdriver.support import expected_conditions as EC


class TestUserAuthenticatedWithFilledDB(FunctionalTestCase):
    def setUp(self):
        super().setUp()
        self.filled_db()
        self.create_user()
        self.client.force_login(self.user)
        self.browser.get(self.live_server_url)

        self.browser.add_cookie({
            'name': 'sessionid',
            'value': self.client.session.session_key,
            'path': '/',
            'domain': 'localhost',
        })
        self.browser.add_cookie({
            'name': 'csrftoken',
            'value': _get_new_csrf_string()
        })

    def test_append_good_in_inventory_from_catalog_and_go_to_page_of_product(self):
        self.browser.get(self.live_server_url + '/books/catalog/all/')

        BUTTON_LOCATOR = ('xpath', f'//button[@id="id_{self.product1.slug}-{self.product1.pk}"]')
        add_button = self.wait.until(EC.element_to_be_clickable(BUTTON_LOCATOR))
        add_button.click()

        REMOVE_BUTTON = ('xpath', f'//button[contains(@class, "remove")]')
        self.wait.until(EC.visibility_of_element_located(REMOVE_BUTTON))

        INVENTORY_LOCATOR = ('xpath', '//a[text()="Коллекция"]')
        self.wait.until(EC.element_to_be_clickable(INVENTORY_LOCATOR)).click()

        ITEM_TITLE = ('xpath', f'//a[text()="{self.product1.name}"]')
        item_product1 = self.wait.until(EC.visibility_of_element_located(ITEM_TITLE))

        assert item_product1.get_attribute('title') == self.product1.name

        item_product1.click()

        PRODUCT_TITLE = ('xpath', '//span[@class="product-title"]')
        assert self.product1.name in self.wait.until(EC.visibility_of_element_located(PRODUCT_TITLE)).text

    def test_append_good_from_product_and_remove_it(self):
        STATUSES = [('3', 'Начато'), ('2', 'Отложенно'), ('1', 'Добавленно'), ('0', 'Прочитанно')]

        self.browser.get(self.live_server_url + '/books/catalog/all')

        PRODUCT_LOCATOR = ('xpath', f'//a[@title="{self.product1.name}"]')
        self.wait.until(EC.element_to_be_clickable(PRODUCT_LOCATOR), 'Catalog page don`t displayed.').click()

        BUTTON_ADD_LOCATOR = ('xpath', f'//button[contains(@class,"btn-add")]')
        self.wait.until(EC.element_to_be_clickable(BUTTON_ADD_LOCATOR), 'Product page don`t displayed.').click()

        self.wait.until(EC.invisibility_of_element(BUTTON_ADD_LOCATOR), 'Add-Button don`t deleted.')

        SELECT_STATUS_LOCATOR = ('xpath', '//select[@class="select-status"]')
        select_status = Select(self.wait.until(EC.element_to_be_clickable(SELECT_STATUS_LOCATOR)))

        for i, status in enumerate(select_status.options):
            assert status.text == STATUSES[i][1], f'Value {status.text} != {STATUSES[i][1]}'

        select_status.select_by_value(STATUSES[-1][0])
        DIV_STATUS_LOCATOR = ('xpath', '//div[contains(@class, "card-status")]')
        assert self.wait.until(EC.visibility_of_element_located(DIV_STATUS_LOCATOR)).text == STATUSES[-1][1]

        RANK_LOCATOR = ('xpath', f'//label[@for="rank_3-{self.product1.slug}"]')
        self.wait.until(EC.element_to_be_clickable(RANK_LOCATOR)).click()

        self.browser.refresh()

        RANK_LOCATOR_BUTTON = ('id', f'rank_3-{self.product1.slug}')
        assert self.wait.until(EC.presence_of_element_located(RANK_LOCATOR_BUTTON)).get_attribute('checked')

        self.wait.until(EC.visibility_of_element_located(SELECT_STATUS_LOCATOR))

        SELECT_OPTION_LOCATOR = ('xpath', '//option[@selected]')

        assert self.wait.until(EC.presence_of_element_located(SELECT_OPTION_LOCATOR)).text == STATUSES[-1][1]

        REMOVE_BUTTON = ('xpath', '//button[contains(@class, "btn-remove")]')
        self.browser.find_element(*REMOVE_BUTTON).click()

        BLOCK_USER_DATA = ('xpath', '//div[@class="user-data"]')
        self.wait.until(EC.invisibility_of_element(BLOCK_USER_DATA))
