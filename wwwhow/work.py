from logging import getLogger
from random import choice

from bs4 import BeautifulSoup

from wwwhow.lib.pull import fetch_entry, image_handle


class Entry(object):
    def __init__(self, args):
        self._log = getLogger(__name__)
        self.pos = args.position
        self.url, html = fetch_entry(args.url)
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
        selection = list(
            self._soup.select(
                'div.mwimg.largeimage'
            )
        )
        if self.pos >= 0 and self.pos <= len(selection):
            self._log.debug('using image element on position %d', self.pos)
            return selection[self.pos]
        return choice(selection)

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

    def _caption_link(self, image_tag):
        self._log.debug('parsing image caption link from image tags')
        return image_tag.parent.select(
            'div.step'
        )[-1].select(
            'b.whb'
        )[-1].select(
            'a'
        )[-1].string

    def __call__(self):
        self._log.debug('collecting fine data from the internet')
        image_tag = self._select_image()
        image_url = self._image_url(image_tag)
        image_name, image_stream = image_handle(image_url)
        caption = self._caption(image_tag)
        if not caption:
            caption = self._caption_link(image_tag)
        return dict(
            url=self.url,
            title=self._title(),
            caption=caption,
            image_name=image_name,
            image_stream=image_stream
        )
