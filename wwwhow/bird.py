from tweepy import API, OAuthHandler


class Robot(object):
    def __init__(self, auth):
        self._auth = OAuthHandler(
            auth.consumer_key, auth.consumer_secret
        )
        self._auth.set_access_token(
            auth.access_token, auth.access_token_secret
        )

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
        status = self._status(entry)
        api = API(self._auth)
        return api.update_with_media(entry.temp, status).id
