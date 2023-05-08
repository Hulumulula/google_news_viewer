import os
import json
import logging
import multiprocessing

from random import choice
from datetime import datetime
from multiprocessing import Pool, Manager
from selenium.common.exceptions import WebDriverException

from core.get_list_url import get_data
from core.selenium_viewer import Viewer
from core.db_scripts import Profile
from settings import (
    HOME_URL,
    SUBHOME_URL,
    PROCESSES,
    HEADERS,
    DEBUG,
)


def main(data: tuple) -> None:
    logger = logging.getLogger(__name__)
    logger.info(f'The process started with id: {os.getpid()}')

    url, user_with_cookies, locker = data
    cookie = json.loads(user_with_cookies[1]) if user_with_cookies[1] else None
    new_cookies = None

    try:
        view = Viewer()
        view.getData(url=url)
        view.addCookie(cookies=cookie)
        view.webScrolling()

        new_cookies = view.getCookies()
        view.quit()

    except WebDriverException as ex:
        logger.error(
            msg=f'Unknown error: {ex.msg}.',
            exc_info=DEBUG
        )

    except BaseException:
        logger.error(msg=f'Error when viewing the news.', exc_info=DEBUG)

    # If the new cookies are any different, we will change them.
    # Cookies in the database are stored in json format.
    if new_cookies and new_cookies != cookie:
        logger.info(msg='Saving new cookies.')
        json_cookie = json.dumps(new_cookies)

        try:
            # Block access to the database.
            # So that only one process can change it;
            # for transaction security.
            with locker:
                with Profile() as db_profile:
                    db_profile.update_one_profile(
                        (
                            json_cookie,                                    # cookie
                            datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  # datetime_last_start
                            int(user_with_cookies[0]),                      # id
                        )
                    )
        except Exception:
            logger.error(msg='Error when saving cookies.', exc_info=DEBUG)

        else:
            logger.info(msg='Cookies have been successfully updated.')

    logger.info(f'The process ended with id: {os.getpid()}')


if __name__ == "__main__":
    globals()['logger'] = multiprocessing.get_logger()

    logger = logging.getLogger(__name__)
    logger.info(msg='The program started working.')

    try:
        # Gets the news
        breaking_news = get_data(url=HOME_URL + SUBHOME_URL, headers=HEADERS)

        if breaking_news:
            logger.info(msg='We\'re looking at the news.')

            # Returns tuple pairs (user_id, cookie).
            # If none, it returns None.
            with Profile() as db_profile:
                users_with_cookies = db_profile.get_users_and_cookies()

            # The manager is needed to lock the database
            # when new cookies are written.
            with Manager() as manager:
                locker = manager.Lock()
                data = list()

                # Collect the list by giving each account a random link.
                # Lock is passed with each function.
                for user in users_with_cookies:
                    data.append((choice(breaking_news), user, locker))

                # map_async implements the map function as asynchronous.
                # Each function is placed to its own process
                # and the processes are placed in Pool.
                with Pool(processes=PROCESSES) as pool:
                    result = pool.map_async(main, data)
                    # Wait for the end of the functions.
                    result.wait()

    except KeyboardInterrupt:
        logger.error(msg='Keyboard Interrupt.', exc_info=DEBUG)

    except BaseException as ex:
        logger.error(msg=f'Base Exception in main module.\nError: {ex.__class__.__name__}', exc_info=DEBUG)

    logger.info(msg='The program is over.')
