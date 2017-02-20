import datetime

from ..base import TimeBaseCommand
from ... import tasks


class Command(TimeBaseCommand):
    help_text = (
        "Count the number of overdue tasks by estimated time"
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_command_line_options(self):
        super(Command, self).add_command_line_options()

    def execute(self, **kwargs):
        super(Command, self).execute(**kwargs)

        overdue_items = tasks.get_overdue(self.todoist_api)

        total_time = 0.0
        for item in overdue_items:
            total_time += self.get_hours_estimate(item)

        if kwargs['debug']:
            print '%d overdue items will take %.2f hours' % (
                len(overdue_items),
                total_time
            )
        else:
            worksheet = self.get_or_create_worksheet(
                'overdue time',
                ['date', 'n', 'time (hours)'],
            )
            worksheet.insert_row([
                datetime.datetime.now().date(),
                len(overdue_items),
                total_time,
            ], 2)
