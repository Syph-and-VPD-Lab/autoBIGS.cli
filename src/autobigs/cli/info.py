from argparse import ArgumentParser, Namespace
import asyncio
import csv
from os import path
from autobigs.engine.analysis.bigsdb import BIGSdbIndex

def setup_parser(parser: ArgumentParser):
    parser.description = "Fetches the latest BIGSdb MLST database definitions."
    
    retrieve_group = parser.add_mutually_exclusive_group(required=True)
    retrieve_group.add_argument(
        "--retrieve-bigsdbs", "-l",
        action="store_true",
        dest="list_dbs",
        required=False,
        default=False,
        help="Lists all known BIGSdb MLST databases (fetched from known APIs and cached)."
    )

    retrieve_group.add_argument(
        "--retrieve-bigsdb-schemes", "-lschemes",
        nargs="+",
        action="extend",
        dest="list_bigsdb_schemes",
        required=False,
        default=[],
        type=str,
        help="Lists the known scheme IDs for a given BIGSdb sequence definition database name. The name, and then the ID of the scheme is given."
    )

    parser.add_argument(
        "--csv", "-o",
        dest="csv_output",
        required=False,
        default=None,
        help="Output list as CSV at a given path. A suffix is added depending on the action taken."
    )

    parser.set_defaults(run=run_asynchronously)
    return parser

async def run(args: Namespace):
    async with BIGSdbIndex() as bigsdb_index:
        if args.list_dbs:
            known_seqdef_dbs = await bigsdb_index.get_known_seqdef_dbs(force=False)
            sorted_seqdef_dbs = [(name, source) for name, source in sorted(known_seqdef_dbs.items())]
            print("The following are all known BIGS database names, and their source (sorted alphabetically):")
            print("\n".join(["{0}: {1}".format(name, source) for name, source in sorted_seqdef_dbs]))
            if args.csv_output:
                with open(args.csv_output, "w") as csv_out_handle:
                    writer = csv.writer(csv_out_handle)
                    writer.writerow(("BIGSdb Names", "Source"))
                    writer.writerows(sorted_seqdef_dbs)
                    print("\nDatabase output written to {0}".format(args.csv_output))

        if args.list_bigsdb_schemes:
            csv_scheme_rows = []
            for bigsdb_scheme_name in args.list_bigsdb_schemes:
                schemes = await bigsdb_index.get_schemes_for_seqdefdb(bigsdb_scheme_name)
                csv_scheme_rows.extend([(name, id, bigsdb_scheme_name) for name, id in sorted(schemes.items())])
                print("The following are the known schemes for \"{0}\", and their associated IDs:".format(bigsdb_scheme_name))
                print("\n".join(["{0}: {1}".format(name, id) for name, id, database in csv_scheme_rows]))
            if args.csv_output:
                with open(args.csv_output, "w") as csv_out_handle:
                    writer = csv.writer(csv_out_handle)
                    writer.writerow(("Name", "ID", "Database Name"))
                    writer.writerows(csv_scheme_rows)
                print("\nscheme list output written to {0}".format(args.csv_output))

def run_asynchronously(args: Namespace):
    asyncio.run(run(args))

