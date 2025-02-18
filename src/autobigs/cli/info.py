from argparse import ArgumentParser, Namespace
import asyncio
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

    parser.set_defaults(run=run_asynchronously)
    return parser

async def run(args: Namespace):
    async with BIGSdbIndex() as bigsdb_index:
        if args.list_dbs:
            known_seqdef_dbs = await bigsdb_index.get_known_seqdef_dbs(force=False)
            print("The following are all known BIGS database names (sorted alphabetically):")
            print("\n".join(sorted(known_seqdef_dbs.keys())))

        for bigsdb_schema_name in args.list_bigsdb_schemas:
            schemas = await bigsdb_index.get_schemas_for_seqdefdb(bigsdb_schema_name)
            print("The following are the known schemas for \"{0}\", and their associated IDs:".format(bigsdb_schema_name))
            for schema_desc, schema_id in schemas.items():
                print(f"{schema_desc}: {schema_id}")

        if not (args.list_dbs or len(args.list_bigsdb_schemas) > 0):
            print("Nothing to do. Try specifying \"-l\" for a list of known databases, or \"-h\" for more information.")

def run_asynchronously(args: Namespace):
    asyncio.run(run(args))

