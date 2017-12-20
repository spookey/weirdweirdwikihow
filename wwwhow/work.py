from logging import getLogger
from random import choice

from bs4 import BeautifulSoup

from wwwhow.lib.pull import load_image, some_entry


class Entry(object):
    def __init__(self, temp):
        self._log = getLogger(__name__)
        self.temp = temp
        self.url, html = some_entry()
        self._soup = BeautifulSoup(html, 'html.parser')
        self.title = None
        self.image = None
        self.caption = None

    def _title(self):
        self._log.debug('parsing entry title')
        return self._soup.select(
            'h1.firstHeading'
        )[-1].select(
            'a'
        )[-1].string

    def __pre_images(self):
        self._log.debug('fetching image tags')
        return self._soup.select(
            'div.mwimg.largeimage'
        )

    def _image_tag(self):
        return choice(list(self.__pre_images()))

    def _image(self, image_tag):
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
        self.title = self._title()
        image_tag = self._image_tag()
        self.image = self._image(image_tag)
        self.caption = self._caption(image_tag)
        load_image(self.image, self.temp)
        return self
