import argparse
import json

from todoist import TodoistAPI


class BaseCommand(object):
    help_text = ''

    def __init__(self, subcommand_creator):

        # keep a local copy of the config file which is useful during
        # autocompletion
        self.config = None

        # set up the subcommand options
        self.subcommand_creator = subcommand_creator
        self.option_parser = self.subcommand_creator.add_parser(
            self.get_command_name(),
            help=self.help_text,
            description=self.help_text,
        )
        self.add_command_line_options()

    def get_command_name(self):
        """The command name defaults to the name of the module."""
        return self.__module__.rsplit('.', 1)[1]

    def add_command_line_options(self):
        self.option_parser.add_argument(
            '--todoist',
            type=argparse.FileType('r'),
            metavar='JSONFILE',
            default='todoist.json',
            help='todoist credentials file in json format',
        )
        self.option_parser.add_argument(
            '--google',
            type=argparse.FileType('r'),
            metavar='JSONFILE',
            default='google.json',
            help='google credentials file in json format',
        )
        self.option_parser.add_argument(
            '--debug',
            action='store_true',
            help='log output on command line, NOT google spreadsheet'
        )

    def execute(self, todoist=None, google=None, debug=None, **kwargs):
        """Common execution workflows are handled here"""

        # create an authenticated instance of the TodoistAPI
        credentials = json.load(todoist)
        self.todoist_api = TodoistAPI(**credentials)

        # authenticate to google
        pass
