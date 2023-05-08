import time
import logging
import requests

from bs4 import BeautifulSoup
from typing import Any

from settings import (
    HOME_URL,
    NAMED_URL,
    DEBUG,
)


logger = logging.getLogger(__name__)


def valid_url(url: str) -> bool:
    """
    Checks if the links to the news are relevant or not.
    """
    try:
        if url.startswith(f'.{NAMED_URL}') or url.startswith(f'{HOME_URL}{NAMED_URL}'):
            return True

    except AttributeError:
        logger.error(msg='URL returned NoneType instead of STR', exc_info=DEBUG)

    except Exception as ex:
        logger.critical(msg='Unexpected error', exc_info=DEBUG)
        raise ex

    return False


def from_named_to_explicit_url(url: str) -> str:
    """
    Makes the link look normal.
    """
    try:
        if url.startswith(f'.{NAMED_URL}'):
            url = HOME_URL + url[1:]

        return url

    except IndexError:
        logger.error(msg='IndexError', exc_info=DEBUG)

    except AttributeError:
        logger.error(msg='AttributeError', exc_info=DEBUG)

    except Exception as ex:
        logger.critical(msg='Unexpected error', exc_info=DEBUG)
        raise ex


def get_data(url: str, headers: dict[Any] = None) -> list:
    """
    Collects news links from news.google.com into a list.
    """

    list_url = set()
    attempt = 1
    logger.info(msg='News gathering begins.')

    while attempt < 5:
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, features="html.parser")

            for item in soup.findAll('a', href=True):
                url_hr = item['href']

                if valid_url(url_hr):
                    list_url.add(from_named_to_explicit_url(url_hr))

            break

        except requests.exceptions.ConnectionError:
            logger.warning(msg='You need a VPN or the requests are too frequent!', exc_info=DEBUG)
            logger.info(f'Attempt {attempt}/5')
            attempt += 1
            time.sleep(5)

        except requests.exceptions.RequestException:
            logger.error(f'Request error with url=\"{url}\"', exc_info=DEBUG)
            logger.info(f'Attempt {attempt}/5')
            attempt += 1
            time.sleep(5)

        except Exception as ex:
            logger.critical(msg='Unexpected error', exc_info=DEBUG)
            raise ex

    if len(list_url) == 0:
        logger.warning('Your news overview is empty.')

    else:
        logger.info('All news was successfully received!')

    return list(list_url)
