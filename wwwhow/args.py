from shared.args import arg_help, base_parser
from shared.conf import URL_RANDOM


def arguments(name):
    parser = base_parser(name)

    parser.add_argument(
        '-t', '--tries', default=9, type=int,
        help=arg_help('maximum number to try get some image')
    )
    parser.add_argument(
        '-u', '--url', default=URL_RANDOM,
        help=arg_help('wikihow entry url')
    )
    parser.add_argument(
        '-p', '--position', default=-1, type=int,
        help=arg_help('zero indexed image position in entry')
    )

    return parser.parse_args()
