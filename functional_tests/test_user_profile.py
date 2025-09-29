from time import sleep

from django.middleware.csrf import _get_new_csrf_string
from selenium.webdriver.support.select import Select

from functional_tests.base import FunctionalTestCase
from selenium.webdriver.support import expected_conditions as EC


class TestUserNotAuthenticated(FunctionalTestCase):

    def test_correct_register_user_this_min_values(self):

        REGISTER_BUTTON_LOCATOR = ('xpath', '//a[text()="Регистрация"]')
        FIELDS_NAME = ['username', 'email', 'password1', 'password2']
        FIELDS_VALUE = ['kapler', 'mypochta@dmail.com', '123carton', '123carton']

        self.browser.get(self.live_server_url)
        self.browser.find_element('xpath', '//a[text()="Sign in"]').click()
        self.wait.until(EC.element_to_be_clickable(REGISTER_BUTTON_LOCATOR)).click()

        for i, name in enumerate(FIELDS_NAME):
            input_field = self.wait.until(EC.element_to_be_clickable(('xpath', f'//input[@name="{name}"]')))
            input_field.send_keys(FIELDS_VALUE[i])

        self.browser.find_element('xpath', '//button[@type="submit"]').click()

        LOGIN_USERNAME = ('xpath', '//input[@id="id_username"]')
        LOGIN_PASSWORD = ('xpath', '//input[@id="id_password"]')
        self.wait.until(EC.visibility_of_element_located(LOGIN_USERNAME)).send_keys(FIELDS_VALUE[0])
        self.wait.until(EC.visibility_of_element_located(LOGIN_PASSWORD)).send_keys(FIELDS_VALUE[2])
        self.browser.find_element('xpath', '//button[@type="submit"]').click()

        img = self.wait.until(EC.element_to_be_clickable(('xpath', '//a[@name="profile-btn"]')))
        profile = self.browser.find_element('xpath', '//a[text()="Профиль"]')

        self.action.move_to_element(img).click(profile).perform()

        USERNAME_LOCATOR = ('xpath', '(//div[@class="profile-content"]//p)[1]')
        EMAIL_LOCATOR = ('xpath', '(//div[@class="profile-content"]//p)[2]')
        assert FIELDS_VALUE[0] in self.wait.until(EC.visibility_of_element_located(USERNAME_LOCATOR)).text
        assert FIELDS_VALUE[1] in self.wait.until(EC.visibility_of_element_located(EMAIL_LOCATOR)).text


class TestUserAuthenticatedWithFilledBD(FunctionalTestCase):
    def setUp(self):
        super().setUp()
        self.filled_db()
        self.create_user()
        self.client.force_login(self.user)
        self.browser.get(self.live_server_url)

        self.browser.add_cookie({
            'name':'sessionid',
            'value': self.client.session.session_key,
            'path':'/',
            'domain':'localhost',
        })
        self.browser.add_cookie({
            'name': 'csrftoken',
            'value': _get_new_csrf_string()
        })




    def test_append_good_in_inventory_from_catalog_and_go_to_page_of_product(self):
        sleep(5)
        self.browser.get(self.live_server_url+'/books/catalog/all/')

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
        STATUSES = [('3','Начато'), ('2','Отложенно'),('1','Добавленно'), ('0','Прочитанно')]

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
