from logging import getLogger

from wwwhow.lib.args import arguments
from wwwhow.lib.auth import Auth
from wwwhow.lib.note import log_setup

LOG = getLogger(__name__)


def run():
    args = arguments()
    log_setup(args.log, args.verbose)
    LOG.info('ready')

    auth = Auth(args.auth)
    if args.conf:
        return auth.renew()

    return 0
