import datetime

from gspread.exceptions import WorksheetNotFound

from ..base import BaseCommand
from ...overdue import get_overdue_items


class Command(BaseCommand):
    help_text = (
        "Count the number of overdue tasks"
    )

    def add_command_line_options(self):
        super(Command, self).add_command_line_options()

    def execute(self, **kwargs):
        super(Command, self).execute(**kwargs)

        overdue_items = get_overdue_items(self.todoist_api)

        if kwargs['debug']:
            print '%d overdue items' % len(overdue_items)
        else:
            worksheet = self.get_or_create_worksheet()
            worksheet.insert_row([
                datetime.datetime.now().date(),
                len(overdue_items),
            ], 2)

    def get_or_create_worksheet(self):

        title = 'overdue n'
        try:
            worksheet = self.gdrive_workbook.worksheet(title)
        except WorksheetNotFound:
            worksheet = self.gdrive_workbook.add_worksheet(title, 1, 26)
            worksheet.insert_row(['date', 'n'])
        return worksheet
