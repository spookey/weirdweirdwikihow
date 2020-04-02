from shared.args import arg_help, base_parser


def arguments(name):
    parser = base_parser(name)

    parser.add_argument(
        '-u', '--unfollow', default=0, type=int, dest='num_unfollow',
        help=arg_help('how many accounts to unfollow at once (0 = unlimited)')
    )
    parser.add_argument(
        '-f', '--follow', default=9, type=int, dest='num_tofollow',
        help=arg_help('how many accounts to follow at once (0 = unlimited)')
    )
    parser.add_argument(
        '-n', '--name', default=None, type=str, dest='account_name',
        help=arg_help('follow up to --follow accounts from @name followers')
    )

    return parser.parse_args()
