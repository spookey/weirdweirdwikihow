from logging import getLogger

from tweepy import OAuthHandler


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
