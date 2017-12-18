from logging import getLogger

from requests import request
from requests.exceptions import RequestException

from wwwhow.lib.conf import URL_RANDOM

LOG = getLogger(__name__)


def some_entry():
    LOG.debug('try to get some random entry')
    try:
        res = request('get', URL_RANDOM)
        res.raise_for_status()
    except RequestException as req_ex:
        LOG.exception(req_ex)
    else:
        if res.ok and res.status_code == 200:
            LOG.debug('succes - got random entry')
            return res.url, res.text
    LOG.error('error fetching random entry')
