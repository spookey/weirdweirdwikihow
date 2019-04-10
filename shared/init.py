from logging import getLogger

from shared.auth import Auth
from shared.note import log_setup

LOG = getLogger(__name__)


def initialize(name, args_func):
    args = args_func(name)
    log_setup(name, args.log, args.verbose)
    LOG.info('ready')

    auth = Auth(args)

    code = auth()
    if code is not None:
        return code, None, None

    return None, args, auth
