#!/usr/bin/env python3

from cli_toolkit.script import Script


if __name__ == '__main__':
    """
    Trivial script example with argument
    """
    script = Script()

    script.add_argument('-t', '--test', help='Test argument')

    args = script.parse_args()
    script.debug(args.test)
