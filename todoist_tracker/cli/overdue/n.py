import arrow

from ..base import BaseCommand

TODOIST_UTC_FORMAT = 'ddd DD MMM YYYY HH:mm:ss ZZ'


class Command(BaseCommand):
    help_text = (
        "Count the number of overdue tasks"
    )

    def add_command_line_options(self):
        super(Command, self).add_command_line_options()

    def execute(self, **kwargs):
        super(Command, self).execute(**kwargs)

        overdue_items = []
        today = arrow.utcnow().to('local').date()
        self.todoist_api.items.sync()
        for item in self.todoist_api.items.all():
            if item['due_date_utc']:
                due_datetime = arrow.get(
                    item['due_date_utc'],
                    [TODOIST_UTC_FORMAT],
                )
                local_due_datetime = due_datetime.to('local')
                local_due_date = local_due_datetime.date()
                if local_due_date <= today:
                    overdue_items.append(item)

        if kwargs['debug']:
            print '%d overdue items' % len(overdue_items)
        else:
            raise NotImplementedError
