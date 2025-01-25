#!/usr/bin/env python3
import argparse

from infrastructure.apps import AssimilateVoiceMemoApp

def main():
    parser = argparse.ArgumentParser(
        description="Personal CLI of Keith Morris."
    )

    # Subparsers (useful for commands, e.g., `cli.py upload` or `cli.py download`)
    subparsers = parser.add_subparsers(title="commands", dest="command")
    
    # Create a subparser for the "upload" command
    upload_parser = subparsers.add_parser("assimilate", help="Assimilate a voice memo into the daily note")
    upload_parser.add_argument("file", help="Local audio file path")
    
    # Parse the arguments
    args = parser.parse_args()

    # Sub-command logic
    if args.command == "assimilate":
      AssimilateVoiceMemoApp.run(args.file)

    else:
        print("No sub-command specified.")

if __name__ == "__main__":
    main()