from ..base import BaseCommand


class Command(BaseCommand):
    help_text = (
        "Check availability over the coming days"
    )

    def add_command_line_options(self):
        super(Command, self).add_command_line_options()

    def execute(self, **kwargs):
        super(Command, self).execute(**kwargs)

        print 'boom'
