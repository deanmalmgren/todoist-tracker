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
