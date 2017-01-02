from ..base import BaseCommand


class Command(BaseCommand):
    help_text = (
        "Count the number of overdue tasks by estimated time"
    )

    def add_command_line_options(self):
        super(Command, self).add_command_line_options()

    def execute(self, **kwargs):
        super(Command, self).execute(**kwargs)
        raise NotImplementedError
