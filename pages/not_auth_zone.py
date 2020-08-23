import allure
import logging
from helpers.general_settings import EMAIL, PASSWORD
from helpers.used_selectors import LOGIN_PAGE_CSS_SELECTORS
from .base import BasePage

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class LoginPage(BasePage):
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        super().__init__(driver=driver, url=self.url)
        logger.debug("LoginPage class is initialized")

    @allure.step("Navigate to login page")
    def open_login_page(self):
        self.open_page()
        # logger.info("Press button to open login page")
        # self.look_for_element(selector=LOGIN_PAGE_CSS_SELECTORS["log_in_button"]).click()

    @allure.step("Enter username")
    def set_username(self):
        logger.debug("Look for username field using '{}' selector".format(LOGIN_PAGE_CSS_SELECTORS["input_login"]))
        login_input = self.look_for_element(selector=LOGIN_PAGE_CSS_SELECTORS["input_login"])
        logger.debug("Email field is found")
        logger.info("Clear email field")
        login_input.clear()
        logger.info("Enter email")
        login_input.send_keys(EMAIL)

    @allure.step("Enter password")
    def set_password(self):
        logger.debug("Look for password field '{}' selector".format(LOGIN_PAGE_CSS_SELECTORS["input_password"]))
        password_input = self.look_for_element(selector=LOGIN_PAGE_CSS_SELECTORS["input_password"])
        logger.debug("Password field is found")
        logger.info("Clear password field")
        password_input.clear()
        logger.info("Enter password")
        password_input.send_keys(PASSWORD)

    @allure.step("Log in")
    def login(self):
        if self.driver.title != "Вход — Habr Account":
            self.open_login_page()
        self.set_username()
        self.set_password()
        logger.info("Press button to authorize")
        self.look_for_element(selector=LOGIN_PAGE_CSS_SELECTORS["authorize_button"]).click()
