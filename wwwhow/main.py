from logging import getLogger

from wwwhow.bird import Robot
from wwwhow.lib.args import arguments
from wwwhow.lib.auth import Auth
from wwwhow.lib.note import log_setup
from wwwhow.work import Entry

LOG = getLogger(__name__)


def run():
    args = arguments()
    log_setup(args.log, args.verbose)
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
