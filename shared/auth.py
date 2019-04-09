from json import dumps, loads
from logging import getLogger
from os import path


class Auth:
    def __init__(self, args):
        self._log = getLogger(self.__class__.__name__)
        self._filename = args.auth
        self._conf = args.conf
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_token_secret = None
        self._log.info('"%s" class created', self.__class__.__name__)
        self.load()

    @property
    def _fields(self):
        return [
            key for key in vars(self).keys() if not key.startswith('_')
        ]

    @property
    def valid(self):
        return all(getattr(self, field, None) for field in self._fields)

    def load(self):
        self._log.debug('load authentification data')
        if not path.exists(self._filename):
            self._log.info(
                'nothing to load - '
                'file "%s" does not exist', self._filename
            )
            return True

        with open(self._filename, 'r') as handle:
            data = loads(handle.read())
            for field in self._fields:
                setattr(self, field, data.get(field, None))
            self._log.debug('loading of "%s" successful', self._filename)
            return True

        self._log.warning('loading of "%s" failed', self._filename)
        return False

    def save(self):
        self._log.debug('save authentification data')
        data = dict(
            (field, getattr(self, field, None))
            for field in self._fields
        )
        with open(self._filename, 'w') as handle:
            length = handle.write(dumps(data, indent=2, sort_keys=True))
            self._log.debug(
                'saving to "%s" successful - '
                '"%d" bytes',
                self._filename, length
            )
            return True

        self._log.warning('saving to "%s" failed', self._filename)
        return False

    def configure(self):
        self._log.debug('renew authentification data')
        for field in self._fields:
            print('|> "{}" ({})'.format(
                field, getattr(self, field, '-')
            ))
            value = input('|> ').strip()
            if value:
                setattr(self, field, value)
        return self.save()

    def __call__(self):
        if self._conf:
            if not self.configure():
                self._log.error('configuration failed')
                return 1
            self._log.info('ok')
            return 0

        if not self.valid:
            self._log.error('no auth data present')
            return 1

        return None
