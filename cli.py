#!/usr/bin/env python3

import os
import sys
import argparse
import cmd2
from cmd2 import style, fg, bg, CommandSet, with_argparser, with_category, with_default_category

from testplan.op import OpTest
from testplan.rp import RpTest


professos_url = "http://localhost:8888/api"
#professos_url = "https://openid.professos/api"


class Cli(cmd2.Cmd):
    DEFAULT_CATEGORY = 'General'

    def __init__(self):
        # add shortcuts
        shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)
        shortcuts.update({'ll': 'list'})

        super().__init__(use_ipython=True,
                         multiline_commands=['orate'],
                         shortcuts=shortcuts)

        self.intro = style('Starting Control Center for Professos!', fg=fg.green, bold=True)
        self.prompt = 'cli> '
        self.default_category = 'Others'

    list_parser = cmd2.Cmd2ArgumentParser('list')
    # list_parser.add_argument('action', choices=['configs', 'results'], help='')
    list_parser.add_argument('target', choices=['op', 'rp'], help='')

    @with_argparser(list_parser)
    @with_category(DEFAULT_CATEGORY)
    def do_list(self, ns: argparse.Namespace):
        """ show available configurations """
        cfg_path = "config/" + ns.target

        self.poutput("\nAvailable configurations:")
        self.poutput("==========================\n")
        for cfg in os.listdir(cfg_path):
            self.poutput(cmd2.style(cfg, fg=cmd2.fg.green))


if __name__ == '__main__':
    print("[*] Professos CLI started")
    app = Cli()
    sys.exit(app.cmdloop())

    parser = argparse.ArgumentParser(description='Professos command line interface.')
    parser.add_argument('config', type=str, help='Configuration to run')
    parser.add_argument('--op', action='store_true',
                    default=False,
                    help='op tests')
    parser.add_argument('--rp', action='store_true',
                        default=False,
                        help='rp tests')
    parser.add_argument('--export', action='store_true',
                        default=False,
                        help='export result to file')
    parser.add_argument('--prepare', action='store_true',
                        default=False,
                        help='prepare only for RP tests')
    parser.add_argument('--test', help="A comma separated list of tests which should run", type=lambda x: x.split(','))
    args = parser.parse_args()

    if args.rp == args.op:   # xor
        print("Choose OP or RP tests")
        sys.exit(-1)

    if not os.path.exists("config/op/" if args.op else "config/rp/" + args.config ):
        print("No configuration found for: ", args.config)
        sys.exit(-1)

    if args.op:
        obj = OpTest(professos_url, args.config)
    else:
        obj = RpTest(professos_url, args.config)

    if args.prepare and args.rp:
        obj.prepare()
        sys.exit(0)

    if args.test:
        obj.run(run_test=args.test, export_results=args.export)
    else:
        obj.run(export_results=args.export)
