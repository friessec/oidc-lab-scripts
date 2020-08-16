import argparse
import cmd2
from cmd2 import CommandSet, with_argparser, with_category, with_default_category

from api.report.generator import ReportGenerator


@with_default_category('Session')
class Commands(CommandSet):

    def __init__(self):
        super().__init__()

    def do_listsessions(self, ns: argparse.Namespace):
        """ show all sessions """
        pass

    def do_start(self, ns: argparse.Namespace):
        """ start a new session """
        self.prepare()

    session_parser = cmd2.Cmd2ArgumentParser('session')
    session_parser.add_argument('name', type=str)

    @with_argparser(session_parser)
    def do_resume(self, ns: argparse.Namespace):
        """ resume a session """
        pass

    config_parser = cmd2.Cmd2ArgumentParser('session')
    config_parser.add_argument('action', choices=['set', 'get', 'list'], help='')

    @with_argparser(config_parser)
    def do_config(self, ns: argparse.Namespace):
        self.cli.poutput('Config')
        if ns.action == 'list':
            self.show_config()
        elif ns.action == 'get':
            pass

    def do_report(self, args):
        """ generates a human readable report"""
        report = ReportGenerator(self.session_dir, self.session_dir + '/report')
        report.load_export("result.json")
        report.generate(self.target_name)
