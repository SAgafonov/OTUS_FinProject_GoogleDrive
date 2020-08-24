from helpers.event_listener import MyListener
from helpers.general_settings import PATH_TO_LOGS
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Executor:
    """
        Define webdriver considering options, desired caps,
        the way how to execute tests either locally, using local grid or in cloud
    """

    def __init__(self, browser: str, executor_url: str, remote_type):
        self._remote_type = remote_type
        self._browser = browser
        self._options = None
        self._caps = None
        self._executor_url = executor_url

    def determine_options(self):
        if self._browser == "chrome":
            caps = DesiredCapabilities.CHROME
            caps["loggingPrefs"] = {"performance": "ALL", "browser": "ALL"}
            options = ChromeOptions()
            # options.add_argument('--headless')
            options.add_argument(
                '--window-size=1200x600')  # Исправляет ошибку, когде не видны элементы фильтра продукта в headless режиме
            options.add_argument('--start-fullscreen')
            options.add_argument('--ignore-certificate-errors')
            options.add_experimental_option("w3c", False)
            self._options = options
            self._caps = caps
        elif self._browser == "firefox":
            options = FirefoxOptions()
            options.add_argument('-headless')
            options.add_argument('-kiosk')  # full-screen mode
            self._options = options
            self._caps = {}

    def determine_webdriver(self):
        self.determine_options()
        if self._remote_type == "local":
            if self._browser == "chrome":
                wd = EventFiringWebDriver(webdriver.Chrome(
                    options=self._options,
                    desired_capabilities=self._caps,
                    service_log_path=PATH_TO_LOGS + "chrome_logs.log"
                ), MyListener()
                )
                return wd
        elif self._remote_type == "selenoid":
            desired_cap = {
                'browserName': self._browser,
                # 'version': "65.0",
                # 'enableVNC': True,
                # 'enableVideo': True,
                # 'enableLog': True,
                'name': "Selenoid"
            }
            self._caps = {**self._caps, **desired_cap}
            wd = webdriver.Remote(command_executor=self._executor_url,
                                  desired_capabilities=self._caps,
                                  options=self._options)
            if not wd:
                raise ValueError("'webdriver' is not defined")
            return wd
