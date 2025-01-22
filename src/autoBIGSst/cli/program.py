import argparse
from importlib import metadata
from os import path
import os

from autoBIGSst.cli import info, st
from autoBIGSst.cli.meta import get_module_base_name
import importlib

root_parser = argparse.ArgumentParser(epilog='Use "%(prog)s info -h" to learn how to get available MLST databases, and their available schemas.'
                                      + ' Once that is done, use "%(prog)s st -h" to learn how to retrieve MLST profiles.'
                                      )
subparsers = root_parser.add_subparsers(required=False)

info.setup_parser(subparsers.add_parser(get_module_base_name(info.__name__)))
st.setup_parser(subparsers.add_parser(get_module_base_name(st.__name__)))

root_parser.add_argument(
    "--version",
    action="store_true",
    default=False,
    required=False,
    help="Displays the autoBIGSst.CLI version, and the autoBIGSst.Engine version."
)


def run():
    args = root_parser.parse_args()
    if args.version:
        print(f'autoBIGSst.CLI is running version {
              metadata.version("autoBIGSst-cli")}.')
        print(f'autoBIGSst.Engine is running version {
              metadata.version("autoBIGSst-engine")}.')
    if hasattr(args, "run"):
        args.run(args)


if __name__ == "__main__":
    run()
