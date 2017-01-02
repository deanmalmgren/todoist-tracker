import argparse

from . import overdue

COMMAND_MODULES = (
    overdue,
)


def get_command_line_parser():
    """Public function for creating a parser to execute all of the commands
    in this sub-package.
    """
    command_line_parser = argparse.ArgumentParser(
        description="calculate and log various todoist statistics",
    )
    subcommand_creator = command_line_parser.add_subparsers(
        title='SUBCOMMANDS',
    )
    for command_module in COMMAND_MODULES:
        command = command_module.Command(subcommand_creator)

        # this sets a default value for the command "option" so
        # that, when this Command is selected by argparse from the
        # command line, we know which common instance it
        # corresponds with. See run_subcommand function below.
        command.option_parser.set_defaults(command=command)
    return command_line_parser


def run_subcommand(args):
    """This function runs the command that is selected by this particular
    subcommand parser.
    """
    command = args.__dict__.pop("command")
    command.execute(**args.__dict__)
