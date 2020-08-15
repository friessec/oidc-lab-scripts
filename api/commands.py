import argparse
import cmd2
from cmd2 import CommandSet, with_argparser, with_category, with_default_category


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
