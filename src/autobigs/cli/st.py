
from argparse import ArgumentParser, Namespace
import asyncio
import datetime
from autobigs.engine.writing import write_mlst_profiles_as_csv
from autobigs.engine.reading import read_multiple_fastas
from autobigs.engine.analysis.bigsdb import BIGSdbIndex, BIGSdbMLSTProfiler

def setup_parser(parser: ArgumentParser):
    parser.description = "Returns MLST exact profile matches."
    parser.add_argument(
        "fastas",
        nargs="+",
        action='extend',
        default=[],
        type=str,
        help="The FASTA files to process. Multiple can be listed."
    )

    parser.add_argument(
        "seqdefdb",
        help="The BIGSdb seqdef database to use for typing."
    )

    scheme_group = parser.add_mutually_exclusive_group()

    scheme_group.add_argument(
        "--scheme-id", "-sid",
        type=int,
        help="The BIGSdb seqdef database scheme ID (integer) to use for typing."
    )

    scheme_group.add_argument(
        "--scheme-name", "-sn",
        type=str,
        help="The BIGSdb seqdef database scheme name (string) to use for typing. If neither this argument, nor the ID equivalent is defined, a scheme ID with name \"MLST\" will be used."
    )

    parser.add_argument(
        "out",
        default=f'./{datetime.datetime.now().strftime(r"%Y%m%d%H%M%S")}',
        help="The output CSV name (.csv will be appended)."
    )

    parser.add_argument(
        "--stop-on-fail", "-sof",
        action="store_true",
        dest="stop_on_fail",
        required=False,
        default=False,
        help="Should the algorithm stop in the case there are no matches (or partial matches when expecting exact matches)."
    )
    parser.set_defaults(run=run_asynchronously)
    return parser

async def run(args: Namespace):
    async with BIGSdbIndex() as bigsdb_index:
        gen_strings = read_multiple_fastas(args.fastas)
        scheme_id_lookup = await bigsdb_index.get_schemes_for_seqdefdb(args.seqdefdb)
        scheme_id = args.scheme_id or args.scheme_name or (scheme_id_lookup)["MLST"]
        scheme_name_lookup = {value: key for key, value in scheme_id_lookup.items()}

        async with await bigsdb_index.build_profiler_from_seqdefdb(False, args.seqdefdb, scheme_id) as mlst_profiler:
            if not isinstance(mlst_profiler, BIGSdbMLSTProfiler):
                raise TypeError("MLST profiler type invalid")
            mlst_profiles = mlst_profiler.profile_multiple_strings(gen_strings, args.stop_on_fail)
            failed = await write_mlst_profiles_as_csv(mlst_profiles, args.out)
            if len(failed) > 0:
                print(f"A total of {len(failed)} IDs failed (no profile found):\n{"\n".join(failed)}")
            print(f"Completed fetching from {args.seqdefdb} for {scheme_name_lookup[scheme_id]}s for {len(args.fastas)} sequences.")

def run_asynchronously(args):
    asyncio.run(run(args))

