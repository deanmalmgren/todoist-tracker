import datetime

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
            worksheet = self.get_or_create_worksheet(
                'overdue n',
                ['date', 'n'],
            )
            worksheet.insert_row([
                datetime.datetime.now().date(),
                len(overdue_items),
            ], 2)
