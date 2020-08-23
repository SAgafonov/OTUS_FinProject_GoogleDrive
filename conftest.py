import logging
import pytest
from helpers.general_settings import PATH_TO_LOGS, URL_TO_TEST
from helpers.create_executor import Executor
from pages.not_auth_zone import LoginPage
from pages.auth_zone import AuthorizedPage
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.action_chains import ActionChains

# Set log level for Selenium and urllib3 to Warning
LOGGER.setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Configure general settings for logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s() - %(message)s',
    filemode='w',   # Rewrite logs
    filename=PATH_TO_LOGS + "logs.log"
)


def pytest_addoption(parser):
    parser.addoption(
        "--remote_type",
        required=False,
        default="local",
        choices=["local", "local_grid", "cloud", "selenoid"],
        help="Defines how to run tests: locally, using grid, cloud service or selenoid. "
             "Available values: local, local_grid, cloud, selenoid"
    )
    parser.addoption(
        "--browser",
        required=False,
        default="chrome",
        choices=["chrome", "firefox"],
        help="Browser to test. Available browsers: Chrome, Firefox"
    )
    parser.addoption(
        "--executor-url",
        required=False,
        default="http://192.168.0.108:4444/wd/hub/",
        help="Defines URL where tests will be executed"
    )


@pytest.fixture(scope="module")
def get_browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="module")
def get_remote_type(request):
    return request.config.getoption("--remote_type")


@pytest.fixture(scope="module")
def get_executor_url(request):
    return request.config.getoption("--executor-url")


@pytest.fixture(scope="class")
def browser_in_use(request, get_browser, get_executor_url, get_remote_type):
    e = Executor(get_browser.lower(), get_executor_url, get_remote_type.lower())
    wd = e.determine_webdriver()
    request.addfinalizer(wd.quit)
    return wd


@pytest.fixture()
def to_perform_action(browser_in_use):
    return ActionChains(browser_in_use)


@pytest.fixture()
def login_page(browser_in_use):
    return LoginPage(browser_in_use, URL_TO_TEST)


@pytest.fixture()
def authorized_user(browser_in_use):
    return AuthorizedPage(browser_in_use, URL_TO_TEST)
