import allure
import logging
from helpers.used_selectors import AUTHORIZED_ZONE_CSS_SELECTORS
from .not_auth_zone import LoginPage

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class AuthorizedPage(LoginPage):
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        super().__init__(driver=driver, url=self.url)
        logger.debug("AuthorizedPage class is initialized")

    def check_if_authorized(self):
        logger.debug("Check if user authorized")
        try:
            self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["user_icon"], timeout=2)
        except:
            logger.debug("User is not logged in. Authorize first")
            self.login()

    def check_if_user_menu_opened(self):
        self.check_if_authorized()
        logger.debug("Check if user's menu is opened")
        if self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["user_icon"], timeout=5,
                                 attribute="aria-expanded") == "false":
            logger.debug("Expand user's menu")
            self.open_user_menu()

    @allure.step("Open user menu")
    def open_user_menu(self):
        logger.debug("Click on user's icon to open user menu")
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["user_icon"]).click()

    @allure.step("Get amount of user menu items")
    def amount_of_user_menu_items(self) -> int:
        return len(self.look_for_elements(selector=AUTHORIZED_ZONE_CSS_SELECTORS["user_menu_items"]))

    @allure.step("Get user nickname from user's menu")
    def user_nickname(self) -> str:
        self.check_if_user_menu_opened()
        return self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["user_menu_nickname"]).text

    @allure.step("Open language settings")
    def open_language_settings(self):
        self.check_if_user_menu_opened()
        logger.debug("Open language settings")
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["language_settings_item"], timeout=6).click()

    @allure.step("Get labels from language settings")
    def get_language_menu_labels(self) -> tuple:
        interface_lang_options = []
        if self.look_for_element(selector="body",
                                 attribute="class") != "nl overlayed":
            logger.debug("Language menu is closed. Open it")
            self.open_language_settings()
        lang_menu_label = self.look_for_element(
            selector=AUTHORIZED_ZONE_CSS_SELECTORS["language_settings_popup_label"]).text
        interface_lang_options.append(
            self.look_for_elements(selector=AUTHORIZED_ZONE_CSS_SELECTORS["interface_language_choice"])[0].text)
        interface_lang_options.append(
            self.look_for_elements(selector=AUTHORIZED_ZONE_CSS_SELECTORS["interface_language_choice"])[1].text)
        self.close_language_settings()
        return lang_menu_label, interface_lang_options

    @allure.step("Close language settings")
    def close_language_settings(self):
        logger.debug("Click 'x' to close language settings")
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["close_language_settings"]).click()

    @allure.step("Change language")
    def change_language(self):
        if self.look_for_element(selector="body",
                                 attribute="class") != "nl overlayed":
            logger.debug("Language menu is closed. Open it")
            self.open_language_settings()
        logger.debug("Choose English language")
        self.look_for_elements(selector=AUTHORIZED_ZONE_CSS_SELECTORS["interface_language_choice"])[1].click()
        return self.get_language_menu_labels()

    @allure.step("Navigate to Settings page")
    def open_settings_page(self):
        self.check_if_user_menu_opened()
        logger.debug("Open Settings page")
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["user_menu_settings_item"]).click()

    @allure.step("Get items from Settings page")
    def get_settings_items(self) -> tuple:
        self.open_settings_page()
        settings_page_title = self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["settings_page_title"]).text
        upload_avatar_button = self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["upload_avatar_button"]).text
        return settings_page_title, upload_avatar_button

    @allure.step("Log out")
    def logout(self):
        self.check_if_authorized()
        self.check_if_user_menu_opened()
        logger.debug("Click on 'Log out' button")
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["log_out"]).click()
