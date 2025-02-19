from argparse import ArgumentParser, Namespace
import asyncio
import csv
from os import path
from autobigs.engine.analysis.bigsdb import BIGSdbIndex

def setup_parser(parser: ArgumentParser):
    parser.description = "Fetches the latest BIGSdb MLST database definitions."
    parser.add_argument(
        "--retrieve-bigsdbs", "-l",
        action="store_true",
        dest="list_dbs",
        required=False,
        default=False,
        help="Lists all known BIGSdb MLST databases (fetched from known APIs and cached)."
    )

    parser.add_argument(
        "--retrieve-bigsdb-schemas", "-lschemas",
        nargs="+",
        action="extend",
        dest="list_bigsdb_schemas",
        required=False,
        default=[],
        type=str,
        help="Lists the known schema IDs for a given BIGSdb sequence definition database name. The name, and then the ID of the schema is given."
    )

    parser.add_argument(
        "--csv-prefix", "-o",
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
                dbs_csv_path = path.splitext(args.csv_output)[0] + "_" + "dbs.csv"
                with open(dbs_csv_path, "w") as csv_out_handle:
                    writer = csv.writer(csv_out_handle)
                    writer.writerow(("BIGSdb Names", "Source"))
                    writer.writerows(sorted_seqdef_dbs)
                    print("\nDatabase output written to {0}".format(dbs_csv_path))

        for bigsdb_schema_name in args.list_bigsdb_schemas:
            schemas = await bigsdb_index.get_schemas_for_seqdefdb(bigsdb_schema_name)
            sorted_schemas = [(name, id) for name, id in sorted(schemas.items())]
            print("The following are the known schemas for \"{0}\", and their associated IDs:".format(bigsdb_schema_name))
            print("\n".join(["{0}: {1}".format(name, id) for name, id in sorted_schemas]))
            if args.csv_output:
                schema_csv_path = path.splitext(args.csv_output)[0] + "_" + "schemas.csv"
                with open(schema_csv_path, "w") as csv_out_handle:
                    writer = csv.writer(csv_out_handle)
                    writer.writerow(("Name", "ID"))
                    writer.writerows(sorted_schemas)
                    print("\nSchema list output written to {0}".format(schema_csv_path))
        if not (args.list_dbs or len(args.list_bigsdb_schemas) > 0):
            print("Nothing to do. Try specifying \"-l\" for a list of known databases, or \"-h\" for more information.")

def run_asynchronously(args: Namespace):
    asyncio.run(run(args))

