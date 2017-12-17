from argparse import ArgumentParser

from wwwhow.defaults import DIR_LOGGING, NAME_APP
from wwwhow.lib.note import LOG_LEVELS


def _help(txt):
    return '{txt} (default: %(default)s)'.format(txt=txt)


def arguments():
    parser = ArgumentParser(
        NAME_APP, add_help=True, epilog='-.-'
    )

    parser.add_argument(
        '-l', '--log', default=DIR_LOGGING,
        help=_help('logging directory')
    )
    parser.add_argument(
        '-v', '--verbose', default='warning',
        choices=LOG_LEVELS.keys(),
        help=_help('logging level')
    )

    return parser.parse_args()
