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
        '''.format(**entry).strip()

    def __call__(self, entry):
        status = self._status(entry)
        return API(self._auth).update_with_media(
            entry['image_name'], status, file=entry['image_stream']
        ).id
