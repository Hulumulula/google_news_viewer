import os
import datetime
import logging

from ast import literal_eval
from pathlib import Path
from dotenv import load_dotenv
from logging.config import dictConfig


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(Path(__file__).resolve().parent)

# Environ
dotenv_path = os.path.join(BASE_DIR, '.env')

# Project Settings
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DB_LOCATION = os.getenv('DB_LOCATION') or os.path.join(BASE_DIR, 'db/profile.sqlite')
WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH') or os.path.join(BASE_DIR, 'driver/chromedriver.exe')

if not os.path.exists(WEBDRIVER_PATH):
    WEBDRIVER_PATH = None

# If DEBUG = True - all errors will return trace
DEBUG = literal_eval(os.getenv('DEBUG') or False)

# In the HOME_URL field, specify the URL from which to parse links.
# Example: 'https://google.com'.
# In the NAMED_URL field, enter the URL where your links start.
# If Empty - all of them will be parsed. Example: '/articles'; None.
# url - '{HOME_URL}{SUBHOME_URL}', will look for
# references of the form  '{HOME_URL}{NAMED_URL}/...'
HOME_URL = os.getenv('HOME_URL') or 'https://news.google.com'
SUBHOME_URL = os.getenv('SUBHOME_URL') or '/home'
NAMED_URL = os.getenv('NAMED_URL') or '/articles'
PROCESSES = int(os.getenv('PROCESSES') or 5)
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                  'Safari/537.36 OPR/97.0.0.0 '
}

# logging
LOGGING = {
    'version': 1,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
            'log_colors': {
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            },
        },
        'format_for_file': {
            'format': "%(asctime)s :: %(levelname)s :: %(funcName)s in %(filename)s (l:%(lineno)d) :: %(message)s",
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'colorlog.StreamHandler',
            'formatter': 'colored',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'format_for_file',
            'filename': f'logs/debug_{datetime.date.today()}.log',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console', 'file'],
            'level': f'{"DEBUG" if DEBUG else "INFO"}',
        },
    }
}

dictConfig(LOGGING)

# If True - the information about the program will be displayed.
IS_LOGGING = literal_eval(os.getenv('IS_LOGGING') or True)

if not IS_LOGGING:
    logging.disable(logging.ERROR)
