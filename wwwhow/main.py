from logging import getLogger

from shared.args import args_wwwhow
from shared.auth import Auth
from shared.conf import NAME_WWWHOW
from shared.note import log_setup
from wwwhow.bird import Robot
from wwwhow.work import Entry

LOG = getLogger(__name__)


def run():
    args = args_wwwhow(NAME_WWWHOW)
    log_setup(NAME_WWWHOW, args.log, args.verbose)
    LOG.info('ready')

    auth = Auth(args)
    code = auth()
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
