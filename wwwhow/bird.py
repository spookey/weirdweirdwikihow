from tweepy import API

from shared.bird import BaseRobot


class Robot(BaseRobot):
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
