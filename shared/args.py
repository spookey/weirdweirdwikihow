from argparse import ArgumentParser

from shared.conf import DIR_LOGS, LOC_AUTH
from shared.note import LOG_LEVELS


def arg_help(txt):
    return '{txt} (default: %(default)s)'.format(txt=txt)


def base_parser(name):
    parser = ArgumentParser(
        name, add_help=True, epilog='-.-'
    )

    parser.add_argument(
        '-l', '--log', default=DIR_LOGS,
        help=arg_help('logging directory - should exist')
    )
    parser.add_argument(
        '-v', '--verbose', default='warning',
        choices=LOG_LEVELS.keys(),
        help=arg_help('logging level')
    )
    parser.add_argument(
        '-a', '--auth', default=LOC_AUTH,
        help=arg_help('authentication file for tweepy')
    )
    parser.add_argument(
        '-c', '--conf', default=False, action='store_true',
        help=arg_help('configure tweepy authentication')
    )

    return parser
