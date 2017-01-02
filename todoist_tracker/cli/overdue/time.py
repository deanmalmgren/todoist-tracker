from pytimeparse.timeparse import timeparse

from ..base import BaseCommand
from ...overdue import get_overdue_items


class Command(BaseCommand):
    help_text = (
        "Count the number of overdue tasks by estimated time"
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self._todoist_labels = None

    def add_command_line_options(self):
        super(Command, self).add_command_line_options()

    def execute(self, **kwargs):
        super(Command, self).execute(**kwargs)

        overdue_items = get_overdue_items(self.todoist_api)

        total_time = 0.0
        for item in overdue_items:
            total_time += self.get_hours_estimate(item)

        if kwargs['debug']:
            print '%d overdue items will take %.2f hours' % (
                len(overdue_items),
                total_time
            )
        else:
            raise NotImplementedError

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
