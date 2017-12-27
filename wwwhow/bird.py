from tweepy import API, OAuthHandler
from logging import getLogger


class Robot(object):
    def __init__(self, auth):
        self._log = getLogger(__name__)
        self._auth = OAuthHandler(
            auth.consumer_key, auth.consumer_secret
        )
        self._auth.set_access_token(
            auth.access_token, auth.access_token_secret
        )

    def _status(self, entry):
        self._log.debug('assembling entry text')
        return '''
"{caption}"

({title})
{url}
        '''.format(**entry).strip()

    def __call__(self, entry):
        self._log.debug('trying to post tweet')
        status = self._status(entry)
        return API(self._auth).update_with_media(
            entry['image_name'], status, file=entry['image_stream']
        ).id
