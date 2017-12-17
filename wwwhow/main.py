from logging import getLogger

from wwwhow.lib.args import arguments
from wwwhow.lib.note import log_setup

LOG = getLogger(__name__)


def run():
    args = arguments()
    log_setup(args.log, args.verbose)

    LOG.info('NaN')

    return 0
