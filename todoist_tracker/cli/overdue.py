import argparse

from .base import BaseCommand


class Command(BaseCommand):
    help_text = (
        "Track statistics on overdue tasks"
    )

    def add_command_line_options(self):
        super(Command, self).add_command_line_options()

        overdue_subparsers = self.option_parser.add_subparsers()
        self.overdue_n_parser = overdue_subparsers.add_parser(
            'n',
        )
        self.overdue_time_parser = overdue_subparsers.add_parser(
            'time',
        )
        self.overdue_priority_parser = overdue_subparsers.add_parser(
            'priority',
        )

    def execute(self, **kwargs):
        super(Command, self).execute(**kwargs)
        print 'boom'
