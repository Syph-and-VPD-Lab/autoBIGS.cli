import argparse
from importlib import metadata
from os import path
import os

from automlst.cli import info, st
from automlst.cli.meta import get_module_base_name
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
    help="Displays the autoMLST.CLI version, and the autoMLST.Engine version."
)


def run():
    args = root_parser.parse_args()
    if args.version:
        print(f'autoMLST.CLI is running version {
              metadata.version("automlst-cli")}.')
        print(f'autoMLST.Engine is running version {
              metadata.version("automlst-engine")}.')
    if hasattr(args, "run"):
        args.run(args)


if __name__ == "__main__":
    run()
