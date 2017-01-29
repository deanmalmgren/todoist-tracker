import argparse

from . import availability
from . import overdue
from .utils import get_command_line_parser

COMMAND_MODULES = (availability, overdue, )


def get_cli_parser():
    command_line_parser = argparse.ArgumentParser(
        description="calculate and log various todoist statistics",
    )
    return get_command_line_parser(command_line_parser, COMMAND_MODULES)


def run_subcommand(args):
    """This function runs the command that is selected by this particular
    subcommand parser.
    """
    command = args.__dict__.pop("command")
    command.execute(**args.__dict__)
