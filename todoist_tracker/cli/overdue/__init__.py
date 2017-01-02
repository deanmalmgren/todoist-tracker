import argparse

from ..base import BaseCommand
from ..utils import get_command_line_parser
from . import n
from . import time
from . import priority

COMMAND_MODULES = (n, time, priority, )


class Command(BaseCommand):
    help_text = (
        "Track statistics on overdue tasks"
    )

    def add_command_line_options(self):
        super(Command, self).add_command_line_options()

        # add subcommands using the same pattern
        self.option_parser = get_command_line_parser(
            command_line_parser=self.option_parser,
            command_modules=COMMAND_MODULES,
        )

    def execute(self, **kwargs):
        super(Command, self).execute(**kwargs)
