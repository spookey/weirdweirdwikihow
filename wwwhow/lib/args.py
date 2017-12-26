from argparse import ArgumentParser

from wwwhow.lib.conf import DIR_LOGS, LOC_AUTH, NAME_APP, URL_RANDOM
from wwwhow.lib.note import LOG_LEVELS


def _help(txt):
    return '{txt} (default: %(default)s)'.format(txt=txt)


def arguments():
    parser = ArgumentParser(
        NAME_APP, add_help=True, epilog='-.-'
    )

    parser.add_argument(
        '-l', '--log', default=DIR_LOGS,
        help=_help('logging directory - should exist')
    )
    parser.add_argument(
        '-v', '--verbose', default='warning',
        choices=LOG_LEVELS.keys(),
        help=_help('logging level')
    )
    parser.add_argument(
        '-a', '--auth', default=LOC_AUTH,
        help=_help('authentication file for tweepy')
    )
    parser.add_argument(
        '-c', '--conf', default=False, action='store_true',
        help=_help('configure tweepy authentication')
    )
    parser.add_argument(
        '-u', '--url', default=URL_RANDOM,
        help=_help('wikihow entry url')
    )

    return parser.parse_args()
