from logging import getLogger
from random import choice

from bs4 import BeautifulSoup

from wwwhow.lib.pull import image_handle, random_entry


class Entry(object):
    def __init__(self):
        self._log = getLogger(__name__)
        self.url, html = random_entry()
        self._soup = BeautifulSoup(html, 'html.parser')

    def _title(self):
        self._log.debug('parsing entry title')
        return self._soup.select(
            'h1.firstHeading'
        )[-1].select(
            'a'
        )[-1].string

    def _select_image(self):
        self._log.debug('selecting some beautiful image element')
        return choice(list(
            self._soup.select(
                'div.mwimg.largeimage'
            )
        ))

    def _image_url(self, image_tag):
        self._log.debug('parsing image url from image tags')
        return image_tag.select(
            'noscript'
        )[-1].select(
            'img'
        )[-1]['src']

    def _caption(self, image_tag):
        self._log.debug('parsing image caption from image tags')
        return image_tag.parent.select(
            'div.step'
        )[-1].select(
            'b.whb'
        )[-1].string

    def __call__(self):
        self._log.debug('collecting fine data from the internet')
        image_tag = self._select_image()
        image_url = self._image_url(image_tag)
        image_name, image_stream = image_handle(image_url)
        return dict(
            url=self.url,
            title=self._title(),
            caption=self._caption(image_tag),
            image_name=image_name,
            image_stream=image_stream
        )
