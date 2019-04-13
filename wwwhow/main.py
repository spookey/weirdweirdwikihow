from logging import getLogger

from shared.conf import NAME_WWWHOW
from shared.init import initialize
from wwwhow.args import arguments
from wwwhow.bird import Robot
from wwwhow.work import Entry

LOG = getLogger(__name__)


def run():
    code, args, auth = initialize(NAME_WWWHOW, arguments)
    if code is not None:
        return code

    work = Entry(args)
    post = work()
    if not post:
        LOG.error('post not present')
        return 1

    bird = Robot(auth)
    if not bird(post):
        LOG.error('posting failed')
        return 1

    LOG.info('ok')
    return 0
