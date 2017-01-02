import argparse


# NOTE: this appears here so we can recursively use this functionality in
# recursive subcommands
def get_command_line_parser(command_line_parser, command_modules):
    """Public function for creating a parser to execute all of the commands
    in this sub-package.
    """
    subcommand_creator = command_line_parser.add_subparsers(
        title='SUBCOMMANDS',
    )
    for command_module in command_modules:
        command = command_module.Command(subcommand_creator)

        # this sets a default value for the command "option" so
        # that, when this Command is selected by argparse from the
        # command line, we know which common instance it
        # corresponds with. See run_subcommand function below.
        command.option_parser.set_defaults(command=command)
    return command_line_parser
