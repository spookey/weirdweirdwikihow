from logging import getLogger

from tweepy import API, OAuthHandler, TweepError


class BaseRobot:
    def __init__(self, auth):
        self._log = getLogger(self.__class__.__name__)
        self._auth = OAuthHandler(
            auth.consumer_key, auth.consumer_secret
        )
        self._auth.set_access_token(
            auth.access_token, auth.access_token_secret
        )
        self._log.info('"%s" class created', self.__class__.__name__)
        self._api = None

    @property
    def api(self):
        if self._api is None:
            self._api = API(self._auth)
            self._log.debug(
                'API object for "%s" class created',
                self.__class__.__name__
            )
        return self._api

    def limits(self):
        result = {}
        for limits in (
                self.api.rate_limit_status() or {}
        ).get('resources', {}).values():
            result.update((
                key, val.get('remaining', 0)
            ) for key, val in limits.items())
        return result

    def limit(self, key):
        return (self.limits() or {}).get(key, 0)

    def safe_get_user(self, ident):
        try:
            return self.api.get_user(ident)
        except TweepError as ex:
            self._log.exception(ex)
        return None
