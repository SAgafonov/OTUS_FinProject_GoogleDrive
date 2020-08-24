import allure
import logging
from helpers.used_selectors import AUTHORIZED_ZONE_CSS_SELECTORS
from helpers.general_settings import SETTINGS_PAGE_TITLE, PATH_TO_AVATAR
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
            logger.info("User is not logged in. Authorize first")
            self.login()

    def check_if_user_menu_opened(self):
        self.check_if_authorized()
        logger.debug("Check if user's menu is opened")
        if self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["user_icon"], timeout=5,
                                 attribute="aria-expanded") == "false":
            logger.info("Expand user's menu")
            self.open_user_menu()

    @allure.step("Open user menu")
    def open_user_menu(self):
        logger.info("Click on user's icon to open user menu")
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
        logger.info("Open language settings")
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["language_settings_item"], timeout=6).click()

    @allure.step("Get labels from language settings")
    def get_language_menu_labels(self) -> tuple:
        """
        Return name of language menu and names of interface languages
        :return: tuple(str, str)
        """
        interface_lang_options = []
        if self.look_for_element(selector="body",
                                 attribute="class") != "nl overlayed":
            logger.info("Language menu is closed. Open it")
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
        logger.info("Click 'x' to close language settings")
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["close_language_settings"]).click()

    @allure.step("Change language")
    def change_language(self):
        if self.look_for_element(selector="body",
                                 attribute="class") != "nl overlayed":
            logger.info("Language menu is closed. Open it")
            self.open_language_settings()
        logger.info("Choose English language")
        self.look_for_elements(selector=AUTHORIZED_ZONE_CSS_SELECTORS["interface_language_choice"])[1].click()
        return self.get_language_menu_labels()

    @allure.step("Navigate to Settings page")
    def open_settings_page(self):
        self.check_if_user_menu_opened()
        try:
            self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["settings_page_title"], timeout=5).text != SETTINGS_PAGE_TITLE
        except:
            logger.info("Open Settings page")
            self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["user_menu_settings_item"]).click()

    @allure.step("Get items from Settings page")
    def get_settings_items(self) -> tuple:
        """
        Return heading of setting page and name of button to upload avatar
        :return: tuple(str, str)
        """
        self.open_settings_page()
        settings_page_title = self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["settings_page_title"]).text
        upload_avatar_button = self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["avatar_button"]).text
        return settings_page_title, upload_avatar_button

    @allure.step("Set location to default state")
    def reset_country(self) -> str:
        """
        Return attribute of element
        :return: str
        """
        self.open_settings_page()
        logger.debug("Find 'Country' drop-down")
        country_drop_down = self.check_if_element_clickable(selector=AUTHORIZED_ZONE_CSS_SELECTORS["country_drop_down"])
        logger.info("Choose default option for country")
        self.select_item(elem=country_drop_down, selector=None).select_by_value("")
        self.driver.implicitly_wait(5)
        return self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS['region_drop_down'], attribute='disabled')

    @allure.step("Choose a country in location")
    def change_country(self):
        self.reset_country()
        logger.info("Select country 'Беларусь'")
        country_drop_down = self.check_if_element_clickable(selector=AUTHORIZED_ZONE_CSS_SELECTORS["country_drop_down"])
        self.select_item(elem=country_drop_down, selector=None).select_by_value("22")
        return self.check_if_element_clickable(selector=AUTHORIZED_ZONE_CSS_SELECTORS["region_drop_down"], attribute="disabled")

    @allure.step("Choose a region in location")
    def change_region(self):
        self.change_country()
        logger.info("Select region 1875")
        region_drop_down = self.check_if_element_clickable(selector=AUTHORIZED_ZONE_CSS_SELECTORS["region_drop_down"])
        self.select_item(elem=region_drop_down, selector=None).select_by_value("1875")
        return self.check_if_element_clickable(selector=AUTHORIZED_ZONE_CSS_SELECTORS["city_drop_down"], attribute="disabled")

    @allure.step("Upload avatar")
    def upload_avatar(self):
        self.open_settings_page()
        logger.info("Upload avatar")
        avatar = self.driver.find_element_by_xpath("//input[@type='file']")
        avatar.send_keys(PATH_TO_AVATAR)
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["avatar_image"], timeout=7)

    @allure.step("Save changes")
    def save_changes(self):
        logger.info("Push 'Save' button")
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["save_settings"]).click()
        logger.debug("Wait for message that changes were saved")
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["save_success_message"])

    @allure.step("Refresh the page")
    def refresh_page(self):
        logger.info("Refresh the page")
        self.driver.refresh()

    def check_if_avatar_in_user_icon(self):
        """
        Upload, save and check if avatar uploaded.
        If success avatar is deleted
        :return:
        """
        self.upload_avatar()
        self.save_changes()
        self.refresh_page()
        try:
            self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["user_icon"] + " img")
            self.remove_avatar()
            return True
        except:
            return False

    @allure.step("Remove avatar")
    def remove_avatar(self):
        logger.debug("Click 'Delete' avatar btn")
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["avatar_button"]).click()
        self.save_changes()

    @allure.step("Log out")
    def logout(self):
        self.check_if_user_menu_opened()
        logger.info("Click on 'Log out' button")
        self.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["log_out"]).click()
