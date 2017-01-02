import argparse


class TodoistTrackerParser(argparse.ArgumentParser):
    """This script uses the Todoist configuration in todoist.json to track
    various things in todoist and store them in a google spreadsheet.
    """

    def __init__(self):
        super(TodoistTrackerParser, self).__init__(
            description=self.__class__.__doc__,
        )

        self.add_argument(
            '--todoist',
            type=argparse.FileType('r'),
            metavar='JSONFILE',
            default='todoist.json',
            help='todoist credentials file in json format',
        )
        self.add_argument(
            '--google',
            type=argparse.FileType('r'),
            metavar='JSONFILE',
            default='google.json',
            help='google credentials file in json format',
        )
        self.add_argument(
            '--debug',
            action='store_true',
            help='log output on command line, NOT google spreadsheet'
        )

        self.subparsers = self.add_subparsers(
            parser_class=argparse.ArgumentParser,
        )
        self.add_overdue_parser()

    def add_overdue_parser(self):
        # TODO: clean this up in subclasses instead of this grossness
        self.overdue_parser = self.subparsers.add_parser('overdue')
        overdue_subparsers = self.overdue_parser.add_subparsers()
        self.overdue_n_parser = overdue_subparsers.add_parser(
            'n',
        )
        self.overdue_time_parser = overdue_subparsers.add_parser(
            'time',
        )
        self.overdue_priority_parser = overdue_subparsers.add_parser(
            'priority',
        )
