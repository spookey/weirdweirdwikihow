from logging import getLogger

from tweepy import API, OAuthHandler


class Robot(object):
    def __init__(self, auth):
        self._log = getLogger(self.__class__.__name__)
        self._auth = OAuthHandler(
            auth.consumer_key, auth.consumer_secret
        )
        self._auth.set_access_token(
            auth.access_token, auth.access_token_secret
        )
        self._log.info('"%s" class created', self.__class__.__name__)

    def _status(self, entry):
        self._log.debug('assembling entry text')
        status = '''
"{caption}"

({title})
{url}
        '''.format(**entry).strip()

        self._log.debug('entry text is very beautiful:\n%s', status)
        return status

    def __call__(self, entry):
        self._log.debug('trying to post tweet')

        tweet = API(self._auth).update_with_media(
            entry['image_name'],
            self._status(entry),
            file=entry['image_stream']
        )

        if not tweet.id:
            self._log.warning('posting did not succeed')
            return False

        self._log.info('posting went well. ID is "%s"', tweet.id)
        return True
