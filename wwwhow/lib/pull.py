from io import SEEK_END, SEEK_SET, BytesIO
from logging import getLogger
from os import path

from requests import codes, request
from requests.exceptions import RequestException

LOG = getLogger(__name__)


def fetch_entry(url):
    LOG.debug('try to get some entry from url "%s"', url)
    try:
        res = request('get', url)
        res.raise_for_status()
    except RequestException as req_ex:
        LOG.exception(req_ex)
    else:
        if res.ok and res.status_code == codes.ok:
            LOG.debug('success - got some entry')
            return res.url, res.text

    LOG.error('error fetching entry - sorry')
    return None, ''


class ImageStream(object):
    def __init__(self, req_iter):
        self._log = getLogger(self.__class__.__name__)
        self._bytes = BytesIO()
        self._iter = req_iter
        self._log.info('"%s" class created', self.__class__.__name__)

    def _load_all(self):
        self._bytes.seek(0, SEEK_END)
        for chunk in self._iter:
            self._bytes.write(chunk)

    def _load_until(self, pos):
        current_pos = self._bytes.seek(0, SEEK_END)
        while current_pos < pos:
            try:
                current_pos = self._bytes.write(next(self._iter))
            except StopIteration:
                break

    def tell(self):
        return self._bytes.tell()

    def read(self, size=None):
        left_at = self.tell()
        if size is None:
            self._load_all()
        else:
            pos = left_at + size
            self._load_until(pos)
        self._bytes.seek(left_at)
        return self._bytes.read(size)

    def seek(self, pos, whence=SEEK_SET):
        if whence == SEEK_END:
            self._load_all()
        else:
            self._bytes.seek(pos, whence)

    def close(self):
        self._bytes.close()


def image_handle(url):
    LOG.debug('try to fetch some image')
    try:
        res = request('get', url, stream=True)
        res.raise_for_status()
    except RequestException as req_ex:
        LOG.exception(req_ex)
    else:
        if res.ok and res.status_code == codes.ok:
            LOG.debug('success - got some beautiful image')
            return path.basename(res.url), ImageStream(res.iter_content(64))

    LOG.error('error fetching beautiful image - sorry')
    return None, None
