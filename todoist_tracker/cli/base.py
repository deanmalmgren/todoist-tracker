import argparse
import json
import os

from todoist import TodoistAPI
import gspread
from gspread.exceptions import WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials
from pytimeparse.timeparse import timeparse


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

        # create an authenticated instance of the TodoistAPI. be sure to store
        # the cached data locally and to nuke the existing sync prior to
        # running. otherwise the number of outdated tasks grows
        credentials = json.load(todoist)
        credentials['cache'] = os.path.join(
            os.getcwd(), '.todoist-tracker-sync/'
        )
        self.todoist_api = TodoistAPI(**credentials)

        # authenticate to google
        google_keys = json.load(google)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            google.name,
            ['https://spreadsheets.google.com/feeds'],
        )
        gdrive = gspread.authorize(credentials)
        self.gdrive_workbook = gdrive.open_by_url(google_keys['workbook_url'])

    def get_or_create_worksheet(self, title, header):
        try:
            worksheet = self.gdrive_workbook.worksheet(title)
        except WorksheetNotFound:
            worksheet = self.gdrive_workbook.add_worksheet(title, 1, 26)
            worksheet.insert_row(header)
        return worksheet


class TimeBaseCommand(BaseCommand):
    """easily calculate the time required for various tasks"""

    def __init__(self, *args, **kwargs):
        super(TimeBaseCommand, self).__init__(*args, **kwargs)
        self._todoist_labels = None

    def get_todoist_labels(self):
        if self._todoist_labels:
            return self._todoist_labels
        labels = self.todoist_api.labels.all()
        self._todoist_labels = {}
        for label in labels:
            self._todoist_labels[label['id']] = label['name']
        return self._todoist_labels

    def get_hours_estimate(self, item):
        labels = self.get_todoist_labels()
        hours = 0.0
        for label_id in item['labels']:
            label = labels[label_id]
            seconds_estimate = timeparse(label)
            if seconds_estimate is not None:
                hours += seconds_estimate / 60.0 / 60.0
        return hours
