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

    auth = Auth(args.auth)
    if args.conf:
        if not auth():
            LOG.error('configuration failed - exiting')
            return 1
        LOG.info('ok')
        return 0

    if not auth.valid:
        LOG.error('no auth data present - exiting')
        return 1

    work = Entry(args)
    post = work()
    if not post:
        LOG.error('post not present - exiting')
        return 1

    bird = Robot(auth)
    if not bird(post):
        LOG.error('posting failed - exiting')
        return 1

    LOG.info('ok')
    return 0
