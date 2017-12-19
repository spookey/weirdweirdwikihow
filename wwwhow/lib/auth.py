from json import dumps, loads
from logging import getLogger
from os import path


class Auth(object):
    def __init__(self, filename):
        self._log = getLogger(__name__)
        self._filename = filename
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_token_secret = None
        self.load()

    @property
    def _fields(self):
        return [
            key for key in vars(self).keys() if not key.startswith('_')
        ]

    def load(self):
        self._log.debug('load authentification data')
        if not path.exists(self._filename):
            return
        with open(self._filename, 'r') as handle:
            data = loads(handle.read())
            for field in self._fields:
                setattr(self, field, data.get(field, None))

    def save(self):
        self._log.debug('save authentification data')
        data = dict(
            (field, getattr(self, field, None))
            for field in self._fields
        )
        with open(self._filename, 'w') as handle:
            handle.write(dumps(data, indent=2, sort_keys=True))
            return 0

    def renew(self):
        self._log.debug('renew authentification data')
        for field in self._fields:
            print('|> "{}" ({})'.format(
                field, getattr(self, field, '-')
            ))
            value = input('|> ').strip()
            if value:
                setattr(self, field, value)
        return self.save()
