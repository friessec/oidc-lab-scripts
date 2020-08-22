import argparse
import cmd2
from cmd2 import CommandSet, with_argparser, with_category, with_default_category

from api.report.generator import ReportGenerator


@with_default_category('Session')
class Commands(CommandSet):
    CATEGORY_SESSION = 'Session'
    CATEGORY_COMMANDS = 'Session Commands'

    def __init__(self):
        super().__init__()

    def do_listsessions(self, ns: argparse.Namespace):
        """ show all sessions """
        pass

    def do_start(self, ns: argparse.Namespace):
        """ start a new session """
        pass

    session_parser = cmd2.Cmd2ArgumentParser(CATEGORY_SESSION)
    session_parser.add_argument('name', type=str)

    @with_argparser(session_parser)
    def do_resume(self, ns: argparse.Namespace):
        """ resume a session """
        pass

    config_parser = cmd2.Cmd2ArgumentParser(CATEGORY_SESSION)
    config_parser.add_argument('--show', action='store_true', help='')
    config_parser.add_argument('--get', action='store_true', help='')
    config_parser.add_argument('--set', action='store_true', help='')
    config_parser.add_argument('variable', nargs='?', help='')

    @with_argparser(config_parser)
    def do_config(self, ns: argparse.Namespace):
        if ns.show:
            self.show_config()
        elif ns.get:
            self.cli.poutput('Get {}'.format(ns.get))
        elif ns.set:
            self.cli.poutput('Set {}'.format(ns.set))
            try:
                (k, v) = ns.variable.split("=", 2)
                print('{} = {}'.format(k,v))
            except ValueError as ex:
                self.cli.poutput('Set must be set as Key=Value')
        else:
            self.cli.perror("")

    @with_category(CATEGORY_COMMANDS)
    def do_report(self, args):
        """ generates a human readable report"""
        report = ReportGenerator(self.session_dir, self.session_dir + '/report')
        report.load_export("result.json")
        report.generate(self.target_name)

    prepare_parser = cmd2.Cmd2ArgumentParser(CATEGORY_COMMANDS)
    prepare_parser.add_argument('test_nr', nargs='?', help='')

    @with_category(CATEGORY_COMMANDS)
    @with_argparser(prepare_parser)
    def do_prepare(self, ns: argparse.Namespace):
        pass