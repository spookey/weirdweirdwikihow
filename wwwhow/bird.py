from tweepy import API, OAuthHandler


class Robot(object):
    def __init__(self, auth, temp):
        self._auth = OAuthHandler(
            auth.consumer_key, auth.consumer_secret
        )
        self._auth.set_access_token(
            auth.access_token, auth.access_token_secret
        )
        self._temp = temp

    @staticmethod
    def _status(entry):
        return '''
"{caption}"

({title})
{url}
        '''.format(
            caption=entry.caption,
            title=entry.title,
            url=entry.url
        ).strip()

    def __call__(self, entry):
        entry()
        status = self._status(entry)
        api = API(self._auth)
        api.update_with_media(self._temp, status)
