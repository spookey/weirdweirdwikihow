from logging import getLogger

from wwwhow.lib.args import arguments
from wwwhow.lib.note import log_setup
from wwwhow.work import Entry

LOG = getLogger(__name__)


def run():
    args = arguments()
    log_setup(args.log, args.verbose)

    elem = Entry()()
    LOG.info(elem.url)
    LOG.info(elem.title)
    LOG.info(elem.image)
    LOG.info(elem.caption)
    return 0
