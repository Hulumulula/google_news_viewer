import time
import random
import logging

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import InvalidCookieDomainException
from selenium.webdriver.chrome.service import Service

from settings import WEBDRIVER_PATH, DEBUG


logger = logging.getLogger(__name__)


class Viewer:
    """
    Controls a browser by sending commands.
    The methods are implemented based on the WebDriver class.
    """
    __WEBDRIVER_PATH = WEBDRIVER_PATH

    def __init__(self):
        options = []

        # Disable WebDriver mod
        # for ChromeDriver version 79.0.3945.16 or over
        options.append('--disable-blink-features=AutomationControlled')

        # # Headless
        # options.append('--headless')
        ...

        # Tries to load the driver in the WEBDRIVER_PATH path
        # if it is not None. Otherwise the manager will
        # download the current version into memory.
        if Viewer.__WEBDRIVER_PATH:
            service = Service(
                    executable_path=Viewer.__WEBDRIVER_PATH,
                    service_args=options
                )

        else:
            service = Service(
                    executable_path=ChromeDriverManager().install(),
                    options=options
                )

        driver = webdriver.Chrome(service=service)
        self.driver = driver

    def quit(self) -> None:
        """
        Exit WebDriver.
        """
        self.driver.close()
        self.driver.quit()

    def getData(self, url: str) -> None:
        """
        Loads a web page in the current browser session.
        """
        self.driver.get(url=url)

    def getCookies(self) -> list[dict]:
        """
        Getting cookies after visiting the link.
        """
        return self.driver.get_cookies()

    def addCookie(self, cookies: dict) -> None:
        """
        Adds a cookie to our session.
        """
        if cookies:
            current_url = self.driver.current_url

            for cookie in cookies:
                try:
                    if cookie['domain'] in current_url:
                        self.driver.add_cookie(cookie)

                except InvalidCookieDomainException:
                    logger.error(msg=f'InvalidCookieDomain, cookie = {cookie}', exc_info=DEBUG)

                except KeyError:
                    logger.error(msg=f'KeyError, cookie = {cookie}', exc_info=DEBUG)

    def webScrolling(self) -> None:
        """
        This method allows you to scroll smoothly
        around the page with a random delay.
        """
        __old_position = 0
        __new_position = None

        while __old_position != __new_position:
            __old_position = __new_position

            # A plug so you don't have to flip through an endless tape.
            if __old_position and __old_position > 10000:
                break

            # A pathetic attempt to humane scrolling:D
            for i in range(random.randint(30, 100)):
                ActionChains(self.driver) \
                    .scroll_by_amount(0, i) \
                    .perform()

            time.sleep(random.randint(1, 3))

            # Returns the current scroll position
            __new_position = self.driver.execute_script(
                """return (window.pageYOffset !== undefined)
                 ? window.pageYOffset : (document.documentElement
                  || document.body.parentNode || document.body).scrollTop;"""
            )
