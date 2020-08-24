import allure
import logging
from helpers.general_settings import LOGIN_FORM_LABEL, NICKNAME, NUMBER_OF_USER_MENU_ITEMS, LANGUAGE_SETTINGS_LABEL, \
    INTERFACE_LANGUAGES, SETTINGS_PAGE_TITLE, UPLOAD_AVATAR_BUTTON
from helpers.used_selectors import LOGIN_PAGE_CSS_SELECTORS, AUTHORIZED_ZONE_CSS_SELECTORS

logger = logging.getLogger(__name__)
logger.setLevel('INFO')


@allure.epic("Not authorized zone")
@allure.feature("Authorization")
class TestAuthorization:

    @allure.title("Sign in form")
    def test_login_form(self, login_page):
        logger.info("<======== Run test_login_form test ========>")
        login_page.open_login_page()
        assert login_page.driver.title == "Вход — Habr Account"
        assert login_page.look_for_element(selector=LOGIN_PAGE_CSS_SELECTORS["login_form_label"]).text == LOGIN_FORM_LABEL
        assert login_page.look_for_element(selector=LOGIN_PAGE_CSS_SELECTORS["input_login"])
        assert login_page.look_for_element(selector=LOGIN_PAGE_CSS_SELECTORS["input_password"])
        assert login_page.look_for_element(selector=LOGIN_PAGE_CSS_SELECTORS["authorize_button"])
        assert login_page.look_for_element(selector=LOGIN_PAGE_CSS_SELECTORS["forgot_password_link"])
        logger.info("========> End test_login_form test <========\n")

    @allure.title("Sign in")
    def test_authorization(self, login_page):
        logger.info("<======== Run authorization test ========>")
        login_page.login()
        assert login_page.look_for_element(selector=AUTHORIZED_ZONE_CSS_SELECTORS["user_icon"])
        logger.info("========> End authorization test <========\n")


@allure.epic("Authorized zone")
@allure.feature("Actions in authorized zone")
class TestAuthorizedZone:

    @allure.title("Check user menu")
    def test_check_user_menu(self, authorized_user):
        logger.info("<======== Run authorization test ========>")
        assert authorized_user.user_nickname() == NICKNAME
        assert authorized_user.amount_of_user_menu_items() == NUMBER_OF_USER_MENU_ITEMS
        logger.info("========> End authorization test <========\n")

    @allure.title("Check language overlay")
    def test_language_settings_popup(self, authorized_user):
        logger.info("<======== Run language_settings_popup test ========>")
        lang_settings_label, interface_langs = authorized_user.get_language_menu_labels()
        assert lang_settings_label == LANGUAGE_SETTINGS_LABEL[0]
        assert interface_langs == INTERFACE_LANGUAGES
        logger.info("========> End language_settings_popup test <========\n")

    @allure.title("Check changing language")
    def test_change_language(self, authorized_user):
        logger.info("<======== Run change_language test ========>")
        lang_settings_label, _ = authorized_user.change_language()
        assert lang_settings_label == LANGUAGE_SETTINGS_LABEL[1]
        logger.info("========> End change_language test <========\n")

    @allure.title("Check settings page")
    def test_check_settings_page(self, authorized_user):
        logger.info("<======== Run check_settings_page test ========>")
        settings_page_title, upload_avatar_button = authorized_user.get_settings_items()
        assert settings_page_title == SETTINGS_PAGE_TITLE
        assert upload_avatar_button == UPLOAD_AVATAR_BUTTON
        logger.info("========> End check_settings_page test <========\n")

    @allure.title("Check that 'Region' is disabled if country is not set")
    def test_default_location(self, authorized_user):
        logger.info("<======== Run default_location test ========>")
        assert authorized_user.reset_country()
        logger.info("========> End default_location test <========\n")

    @allure.title("Check changing the location")
    def test_change_location(self, authorized_user):
        logger.info("<======== Run change_location test ========>")
        assert not authorized_user.change_country()
        logger.info("========> End change_location test <========\n")

    @allure.title("Check changing the region")
    def test_change_region(self, authorized_user):
        logger.info("<======== Run change_region test ========>")
        assert not authorized_user.change_region()
        logger.info("========> End change_region test <========\n")

    @allure.title("Check uploading the avatar")
    def test_change_avatar(self, authorized_user):
        logger.info("<======== Run change_avatar test ========>")
        assert authorized_user.check_if_avatar_in_user_icon()
        logger.info("========> End change_avatar test <========\n")

    @allure.title("Log out")
    def test_logout(self, authorized_user):
        logger.info("<======== Run logout test ========>")
        authorized_user.logout()
        assert authorized_user.look_for_element(selector=LOGIN_PAGE_CSS_SELECTORS["log_in_button"])
        logger.info("========> End logout test <========\n")
