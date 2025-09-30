import re
from time import sleep

from django.core import mail
from django.middleware.csrf import _get_new_csrf_string
from selenium.webdriver import Keys
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

    def test_change_password(self):
        NEW_PASSWORD = "moi_pass234"
        self.create_user()
        self.browser.get(self.live_server_url)

        LOG_IN_BATTON_LOCATOR = ('xpath', '//a[text()="Войти"]')
        self.wait.until(EC.element_to_be_clickable(LOG_IN_BATTON_LOCATOR)).click()

        FORGOT_PASSWORD_LOCATOR = ('xpath', '//a[@name="forgot_password"]')
        self.wait.until(EC.element_to_be_clickable(FORGOT_PASSWORD_LOCATOR)).click()

        EMAIL_INPUT_LOCATOR = ('xpath', '//input[@name="email"]')
        email_input = self.wait.until(EC.element_to_be_clickable(EMAIL_INPUT_LOCATOR))
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)

        self.wait.until(EC.title_contains('отправлено'))

        message = mail.outbox[0]
        link = re.search(r'https?://.*/accounts/password-reset/.*/', message.body)
        assert link
        assert self.username in message.body

        self.browser.get(link.group(0))

        NEW_PASSWORD1_LOCATOR = ('xpath', '//input[@name="new_password1"]')
        NEW_PASSWORD2_LOCATOR = ('xpath', '//input[@name="new_password2"]')
        self.wait.until(EC.element_to_be_clickable(NEW_PASSWORD1_LOCATOR)).send_keys(NEW_PASSWORD)
        new_password2_input = self.wait.until(EC.element_to_be_clickable(NEW_PASSWORD2_LOCATOR))
        new_password2_input.send_keys(NEW_PASSWORD)
        new_password2_input.send_keys(Keys.ENTER)

        assert self.wait.until(EC.title_is('Восстановление пароля завершено'))
        self.browser.find_element(*LOG_IN_BATTON_LOCATOR).click()

        INPUT_USERNAME_LOCATOR = ('xpath', '//input[@name="username"]')
        INPUT_PASSWORD_LOCATOR = ('xpath', '//input[@name="password"]')
        self.wait.until(EC.visibility_of_element_located(INPUT_USERNAME_LOCATOR)).send_keys(self.username)
        password_input = self.wait.until(EC.visibility_of_element_located(INPUT_PASSWORD_LOCATOR))
        password_input.send_keys(NEW_PASSWORD)
        password_input.send_keys(Keys.ENTER)

        IMG_PROFILE_LOCATOR = ('xpath', '//img[@class="img-profile"]')
        self.wait.until(EC.visibility_of_element_located(IMG_PROFILE_LOCATOR))


