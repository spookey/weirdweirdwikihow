from argparse import ArgumentParser

from shared.conf import DIR_LOGS, LOC_AUTH, URL_RANDOM
from shared.note import LOG_LEVELS


def _help(txt):
    return '{txt} (default: %(default)s)'.format(txt=txt)


def _base_parser(name):
    parser = ArgumentParser(
        name, add_help=True, epilog='-.-'
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

    return parser


def args_wwwhow(name):
    parser = _base_parser(name)

    parser.add_argument(
        '-t', '--tries', default=9, type=int,
        help=_help('maximum number to try get some image')
    )
    parser.add_argument(
        '-u', '--url', default=URL_RANDOM,
        help=_help('wikihow entry url')
    )
    parser.add_argument(
        '-p', '--position', default=-1, type=int,
        help=_help('zero indexed image position in entry')
    )

    return parser.parse_args()
