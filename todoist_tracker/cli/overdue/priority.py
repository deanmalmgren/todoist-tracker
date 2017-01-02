from ..base import BaseCommand
from ...overdue import get_overdue_items


class Command(BaseCommand):
    help_text = (
        "Count the number of overdue tasks by priority"
    )

    def add_command_line_options(self):
        super(Command, self).add_command_line_options()

    def execute(self, **kwargs):
        super(Command, self).execute(**kwargs)

        overdue_items = get_overdue_items(self.todoist_api)

        counter = {'p1': 0, 'p2': 0, 'p3': 0, 'p4': 0}
        for item in overdue_items:
            priority = 'p' + str(4 - item['priority'] + 1)
            counter[priority] += 1

        if kwargs['debug']:
            for priority, count in sorted(counter.iteritems()):
                print '%4d overdue %s priority items' % (count, priority)
            print '-' * 30
            print '%4d overdue items TOTAL' % len(overdue_items)
        else:
            raise NotImplementedError
