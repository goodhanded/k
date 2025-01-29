import argparse
import yaml

from domain.util.module_resolution import resolve_module
from infrastructure.di import Container, load_definitions_from_yaml
from domain.util.yaml import load_yaml

COMMANDS_YAML_PATH = "commands.yaml"
SERVICES_YAML_PATH = "services.yaml"

def load_and_run():
    definitions = load_definitions_from_yaml(SERVICES_YAML_PATH)
    container = Container(definitions)

    commands = load_yaml(COMMANDS_YAML_PATH, "commands")

    parser = argparse.ArgumentParser(description="Personal CLI of Keith Morris.")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    for cmd_name, cmd_info in commands.items():
        subparser = subparsers.add_parser(cmd_name, help=cmd_info.get("help", ""))

        # If subcommands exist, create another subparser
        if "subcommands" in cmd_info:
            subsubparsers = subparser.add_subparsers(title="subcommands", dest="subcommand")
            for sub_name, sub_info in cmd_info["subcommands"].items():
                sub_subparser = subsubparsers.add_parser(sub_name, help=sub_info.get("help", ""))
                for arg_name, arg_help in sub_info.get("arguments", {}).items():
                    sub_subparser.add_argument(arg_name, help=arg_help)
        else:
            for arg_name, arg_help in cmd_info.get("arguments", {}).items():
                subparser.add_argument(arg_name, help=arg_help)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    # Handle commands and subcommands
    cmd_info = commands.get(args.command, {})
    if "subcommands" in cmd_info and args.subcommand:
        sub_info = cmd_info["subcommands"].get(args.subcommand)
        if not sub_info:
            parser.print_help()
            return
        func = resolve_module(sub_info["target"], container)
    else:
        if not cmd_info.get("target"):
            parser.print_help()
            return
        func = resolve_module(cmd_info["target"], container)

    args_dict = vars(args)
    args_dict.pop("command", None)
    args_dict.pop("subcommand", None)

    func(**args_dict)