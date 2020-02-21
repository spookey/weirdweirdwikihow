from logging import getLogger
from random import choice

from bs4 import BeautifulSoup

from wwwhow.pull import fetch_entry, image_handle


class Entry:
    def __init__(self, args):
        self._log = getLogger(self.__class__.__name__)
        self.pos = args.position
        self.tries = abs(args.tries)
        self.url, html = fetch_entry(args.url)
        self._soup = BeautifulSoup(html, 'html.parser')
        self._log.info('"%s" class created', self.__class__.__name__)

    def _title(self):
        self._log.debug('parsing entry title')

        first_heading = self._soup.select('h1.firstHeading')
        if not first_heading:
            self._log.warning('no first heading present')
            return None

        first_link = first_heading[-1].select('a')
        if not first_link:
            self._log.warning('no link in first heading present')
            return None

        return first_link[-1].string

    def _get_image_tag(self):
        self._log.debug('selecting some beautiful image element')
        selection = list(
            self._soup.select('div.mwimg.largeimage')
        )
        if self.pos >= 0 and self.pos <= len(selection):
            self._log.info('using image element on position "%d"', self.pos)
            return selection[self.pos]
        return choice(selection)

    def _image_url(self, image_tag):
        self._log.debug('parsing image url from image tags')

        img_noscript = image_tag.select('noscript')
        if not img_noscript:
            self._log.warning('no noscript element in image tag present')
            return None

        img_element = img_noscript[-1].select('img')
        if not img_element:
            self._log.warning('no img element in image tag present')
            return None

        return img_element[-1]['src']

    def _image_caption(self, image_tag):
        self._log.debug('parsing image caption text from image tags')

        div_step = image_tag.parent.select('div.step')
        if not div_step:
            self._log.warning('no step div after image tag present')
            return None

        div_caption = div_step[-1].select('b.whb')
        if not div_caption:
            self._log.warning('no bold caption in step div present')
            return None

        text = div_caption[-1].string
        if text:
            return text
        self._log.info('no text caption available - trying link caption')

        div_link = div_caption[-1].select('a')
        if not div_link:
            self._log.warning('no link in bold caption present')
            return None

        return div_link[-1].string

    def work(self):
        self._log.debug('collecting fine data from the internet')

        url = self.url
        if not url:
            self._log.warning('url not present')
            return None

        title = self._title()
        if not title:
            self._log.warning('title not present')
            return None

        image_tag = self._get_image_tag()
        if not image_tag:
            self._log.warning('image tag not present')
            return None

        image_url = self._image_url(image_tag)
        if not image_url:
            self._log.warning('image url not present in image tag')
            return None

        image_name, image_stream = image_handle(image_url)
        if not image_name or not image_stream:
            self._log.warning('image name or stream not present for image url')
            return None

        caption = self._image_caption(image_tag)
        if not caption:
            self._log.warning('image caption not present near image tag')
            return None

        return dict(
            url=url,
            title=title,
            caption=caption,
            image_name=image_name,
            image_stream=image_stream
        )

    def __call__(self):
        for attempt in range(self.tries):
            result = self.work()
            if result:
                self._log.info('retrieving successful')
                return result
            self._log.warning(
                'attempt "%d/%d" failed', 1 + attempt, self.tries
            )

        self._log.error(
            'impossible to retrieve data in "%d" attempts for "%s" - '
            'giving up',
            self.tries, self.url
        )
        return None
