from logging import getLogger

from shared.conf import NAME_TWFOLL
from shared.init import initialize
from twfoll.args import arguments
from twfoll.bird import Robot

LOG = getLogger(__name__)


def run():
    code, args, auth = initialize(NAME_TWFOLL, arguments)
    if code is not None:
        return code

    bird = Robot(auth)
    if not bird(args.num_unfollow, args.num_tofollow, args.account_name):
        LOG.error('follow failed')
        return 1

    LOG.info('ok')
    return 0
