from os import path

from requests.compat import quote_plus, urljoin

NAME_APP = 'weirdweirdwikihow'

DIR_LIB = path.abspath(path.dirname(__file__))
DIR_SRC = path.abspath(path.dirname(DIR_LIB))
DIR_ROOT = path.abspath(path.dirname(DIR_SRC))

DIR_LOGS = path.join(DIR_ROOT, 'logs')

URL_BASE = 'https://www.wikihow.com/'
URL_RANDOM = urljoin(URL_BASE, quote_plus('Special:Randomizer'))

LOC_AUTH = path.join(DIR_ROOT, 'auth.json')
