import argparse
import yaml

from domain.util.module_resolution import resolve_module
from infrastructure.di import Container, load_definitions_from_yaml

def load_and_run():
    """
    Load the commands from commands.yaml and run the selected command.
    """

    definitions = load_definitions_from_yaml('services.yaml')
    container = Container(definitions)

    # Load the YAML
    with open("commands.yaml") as f:
        commands_config = yaml.safe_load(f)

    commands = commands_config["commands"]  # a dict of {command_name: info}

    parser = argparse.ArgumentParser(
        description="Personal CLI of Keith Morris."
    )
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Build subparsers dynamically
    for cmd_name, cmd_info in commands.items():
        subparser = subparsers.add_parser(cmd_name, help=cmd_info["help"])
        for arg_name, arg_help in cmd_info.get("arguments", {}).items():
            subparser.add_argument(arg_name, help=arg_help)

    # Parse the arguments
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    # Look up the selected command's info by name
    cmd_info = commands.get(args.command)
    if not cmd_info:
        parser.print_help()
        return

    func = resolve_module(cmd_info["target"], container)

    # Prepare to call the function
    args_dict = vars(args)
    del args_dict["command"]

    # Call the method with CLI arguments
    func(**args_dict)