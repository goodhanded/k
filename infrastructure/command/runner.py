import argparse
import json
from textwrap import indent

from domain.util.module_resolution import resolve_module
from infrastructure.di import Container, load_definitions_from_yaml
from domain.util.yaml import load_yaml

COMMANDS_YAML_PATH = "/Users/keith/Projects/k/commands.yaml"
SERVICES_YAML_PATH = "/Users/keith/Projects/k/services.yaml"


def build_subcommands(subparsers, commands_dict):
    """
    Recursively add commands (and subcommands) to the parser.
    
    :param subparsers: an argparse._SubParsersAction object
    :param commands_dict: dictionary describing commands and subcommands from YAML
    """
    for cmd_name, cmd_info in commands_dict.items():
        help_text = cmd_info.get("help", "")
        # Create a subparser for this command
        subparser = subparsers.add_parser(cmd_name, help=help_text)

        # If this command has a "target", store it so we can call it later
        if "target" in cmd_info:
            subparser.set_defaults(target=cmd_info["target"])

        # Optional flags, e.g. print_result, print_map, etc.
        if "print_result" in cmd_info:
            subparser.set_defaults(print_result=cmd_info["print_result"])
        if "print_map" in cmd_info:
            subparser.set_defaults(print_map=cmd_info["print_map"])

        # Add arguments if any
        for arg_name, arg_help in cmd_info.get("arguments", {}).items():
            subparser.add_argument(arg_name, help=arg_help)

        # If there are nested subcommands, recursively build them
        if "subcommands" in cmd_info:
            nested_subparsers = subparser.add_subparsers(dest=f"{cmd_name}_subcommand")
            build_subcommands(nested_subparsers, cmd_info["subcommands"])


def format_result(result, print_map):
    """
    Example format function that handles a few output formats:
    - "table"
    - "json"
    
    `print_map` can look like:
      print_map:
        format: "table" or "json"
        columns: [field1, field2, ...]
        order_by: <field_to_sort_on>
        header: "true" or "false"
    
    Adjust this logic to match your return object structure.
    """
    fmt = print_map.get("format", "table")
    columns = print_map.get("columns", [])
    order_by = print_map.get("order_by", None)
    print_header = print_map.get("header", "true") == "true"

    # Extract the main data list. If your result is a custom object with .data, use that.
    if hasattr(result, "data"):
        data = result.data
    elif isinstance(result, list):
        data = result
    else:
        # Fallback if it's a single object or unknown structure
        return str(result)


    # If order_by is present, sort the data
    if order_by:
        # Distinguish between dicts vs. objects
        def get_key_value(item):
            if isinstance(item, dict):
                return item.get(order_by)
            else:
                return getattr(item, order_by, None)

        data = sorted(data, key=get_key_value)

    if fmt == "json":
        # Dump the entire data array to JSON
        return json.dumps(data, indent=2, default=str)

    elif fmt == "table":
        # Basic text table with specified columns
        if not columns:
            # If no columns are specified, just str() the entire data
            return str(data)

        lines = []
        header = " | ".join(columns)
        separator = "-" * len(header)
        
        if print_header:
            lines.append(header)
            lines.append(separator)

        for item in data:
            row_cells = []
            for col in columns:
                # If item is an object, use getattr
                val = getattr(item, col, None)
                # If item is a dict, you might do item.get(col)
                row_cells.append(str(val))
            line = " | ".join(row_cells)
            lines.append(line)

        return "\n".join(lines)

    # Fallback for unknown format
    return str(result)


def load_and_run():
    definitions = load_definitions_from_yaml(SERVICES_YAML_PATH)
    container = Container(definitions)

    commands_dict = load_yaml(COMMANDS_YAML_PATH, "commands")
    parser = argparse.ArgumentParser(description="Personal CLI of Keith Morris.")
    subparsers = parser.add_subparsers(dest="top_command")

    build_subcommands(subparsers, commands_dict)
    args = parser.parse_args()

    if not args.top_command:
        parser.print_help()
        return

    target = getattr(args, "target", None)
    if not target:
        parser.print_help()
        return

    func = resolve_module(target, container)

    # Copy argparse results into a dict
    args_dict = vars(args).copy()

    # Remove special keys we don't want to pass to the function
    print_result = args_dict.pop("print_result", False)
    print_map = args_dict.pop("print_map", None)
    args_dict.pop("target", None)
    # <-- NEW: remove the top_command key
    args_dict.pop("top_command", None)

    # Remove any subcommand placeholders (get_subcommand, openai_subcommand, etc.)
    for key in list(args_dict.keys()):
        if key.endswith("_subcommand"):
            args_dict.pop(key)

    result = func(**args_dict)

    if print_result:
        if print_map:
            # Format output if print_map is defined
            formatted = format_result(result, print_map)
            print(formatted)
        else:
            print(result)


if __name__ == "__main__":
    load_and_run()