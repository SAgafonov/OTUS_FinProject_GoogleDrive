from helpers.event_listener import MyListener
from helpers.general_settings import PATH_TO_LOGS
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, FirefoxProfile
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
            # options.add_argument("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36")
            # options.add_argument("Accept-Language: ru,en-US;q=0.9,en;q=0.8")
            # options.add_argument("Accept-Encoding: gzip, deflate, br")
            # options.add_argument("Accept: */*")
            # options.add_argument("cookie: CONSENT=YES+BY.ru+202003; 1P_JAR=2020-08-23-14; SEARCH_SAMESITE=CgQIwZAB; ACCOUNT_CHOOSER=AFx_qI6CpPWIneXOGTSdoRkEdLYfZOpvULdXmg-5QL3jv2-7FhXefzijLKlMH5m6FHmCt3mHzgUlqyoe55RGP2I9LGpfz-dXJnPaC8mm34Z5sB7GNDRffsBC1dThfju_zkJy0heguzyDK73Ai3UGByMyB3C9UqAIeg; NID=204=BrhA6ED2VJgNVVP0YgpypICDY3ogcST69K2wZ5JQ1VVX_JoDe8xswIAylJyCH6Ydc4MYoiMLP6EcuuYXmCkKdt6MJkqdqXJMhBsOQncYT6K9-bnmfyMGBxlLV9Necaib841AFVS_T5ty9ReVLgDsecatE93wcAEzEw3oERxAlQA; GAPS=1:QU1k3BN0Lq8bOLjRdr_BFpzftzBq5RC_QwoygfJ6LgrPcad30-An8bAS1ohVclHQnYrzV-JRVcKIrL9-QPCvFt8ffYHLZQ:yW761pGrBz8lCc32; __Host-GAPS=1:QU1k3BN0Lq8bOLjRdr_BFpzftzBq5RC_QwoygfJ6LgrPcad30-An8bAS1ohVclHQnYrzV-JRVcKIrL9-QPCvFt8ffYHLZQ:yW761pGrBz8lCc32")

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
        else:
            desired_cap = {
                'browserName': self._browser,
                # 'version': "65.0",
                'enableVNC': True,
                'enableVideo': True,
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
