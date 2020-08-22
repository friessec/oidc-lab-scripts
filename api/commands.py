import os
import argparse
import cmd2
import requests
import sys
from cmd2 import CommandSet, with_argparser, with_category, with_default_category
from datetime import datetime

from api.report.generator import ReportGenerator


@with_default_category('Session')
class Commands(CommandSet):
    CATEGORY_SESSION = 'Session'
    CATEGORY_COMMANDS = 'Session Commands'

    def __init__(self):
        super().__init__()

    def do_listsessions(self, ns: argparse.Namespace):
        """ show all sessions """
        self.cli.poutput("\nAvailable sessions:")
        self.cli.poutput("==========================\n")
        if not os.path.exists(self.result_dir):
            return
        for session in os.listdir(self.result_dir):
            if session == self.session_name:
                self.cli.poutput(cmd2.style('* ' + session, fg=cmd2.fg.green, bold=True))
            else:
                self.cli.poutput(cmd2.style(session, fg=cmd2.fg.green))

    session_start_parser = cmd2.Cmd2ArgumentParser(CATEGORY_SESSION)
    session_start_parser.add_argument('--timestamp', action='store_true', help='')
    session_start_parser.add_argument('--name', type=str)

    @with_argparser(session_start_parser)
    def do_start(self, ns: argparse.Namespace):
        """ start a new session """
        if not ns.name and not ns.timestamp:
            self.session_name = 'default'
        elif ns.name:
            self.session_name = ns.name
        elif ns.timestamp:
            self.session_name = datetime.now().isoformat(timespec='minutes')
        self.cli.poutput("Start session {}".format(self.session_name))
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir)

    session_resume_parser = cmd2.Cmd2ArgumentParser(CATEGORY_SESSION)
    session_resume_parser.add_argument('name', type=str)

    @with_argparser(session_resume_parser)
    def do_resume(self, ns: argparse.Namespace):
        """ resume a session """
        if not os.path.exists(self.result_dir + '/' + ns.name):
            self.cli.poutput(cmd2.style('No session found with name {}'.format(ns.name), fg=cmd2.fg.red))
        else:
            self.session_name = ns.name

    config_parser = cmd2.Cmd2ArgumentParser(CATEGORY_SESSION)
    config_parser.add_argument('--show', action='store_true', help='')
    config_parser.add_argument('--get', action='store_true', help='')
    config_parser.add_argument('--set', action='store_true', help='')
    config_parser.add_argument('variable', nargs='?', help='')

    @with_argparser(config_parser)
    def do_config(self, ns: argparse.Namespace):
        if not ns.show and not ns.get and not ns.set:
            self.show_config()
        elif ns.show:
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

    @with_category(CATEGORY_COMMANDS)
    def do_create(self, args):
        """ create a new professos test id """
        try:
            self.create()
        except requests.RequestException as e:
            self.cli.poutput("Received error from Professos?")

    prepare_parser = cmd2.Cmd2ArgumentParser(CATEGORY_COMMANDS)
    prepare_parser.add_argument('--test', type=int, help='')

    @with_category(CATEGORY_COMMANDS)
    @with_argparser(prepare_parser)
    def do_prepare(self, ns: argparse.Namespace):
        pass