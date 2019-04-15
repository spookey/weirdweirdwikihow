from os import path

from requests.compat import quote_plus, urljoin

NAME_WWWHOW = 'weirdweirdwikihow'
NAME_TWFOLL = 'twitterfollow'

DIR_ROOT = path.abspath(path.dirname(path.dirname(__file__)))

DIR_LOGS = path.join(DIR_ROOT, 'logs')
LOC_AUTH = path.join(DIR_ROOT, 'auth.json')

URL_BASE = 'https://www.wikihow.com/'
URL_RANDOM = urljoin(URL_BASE, quote_plus('Special:Randomizer'))

CODES_PASS = [
    160
]
