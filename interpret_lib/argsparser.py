import argparse
import sys
import os
from interpret_lib.errorhandler import MissingArgError, InputFileError


def args_parser():
    def check_stats_arg(arg):
        if arg:
            if not args.stats:
                raise MissingArgError("Stats flag has not been provided")
            return True
        return False

    parser = argparse.ArgumentParser(description="Interpreter for IPPCode21")
    parser.add_argument("--source", nargs=1, help="XML file")
    parser.add_argument("--input", nargs=1, help="File for interpeter")

    parser.add_argument("--stats", nargs=1, help="Collecting interpreter's statistics")
    parser.add_argument(
        "--insts",
        action="store_true",
        help="Number of called instructions (Debug instructions and Label are not considered)",
    )
    parser.add_argument(
        "--hot",
        action="store_true",
        help="The most called instruction with least order number",
    )
    parser.add_argument(
        "--vars",
        action="store_true",
        help="Number of initialized variables in all Frames",
    )

    args = parser.parse_args()

    source_file = None
    input_file = None

    stats = {"file": None, "insts": False, "hot": False, "vars": False}

    try:
        if not args.source and not args.input:
            raise MissingArgError

        if args.source:
            source_file = args.source[0]

        if args.input:
            if not os.path.isfile(args.input[0]):
                raise InputFileError
            input_file = args.input[0]

        if args.stats:
            stats["file"] = args.stats[0]

        stats["insts"] = check_stats_arg(args.insts)
        stats["hot"] = check_stats_arg(args.hot)
        stats["vars"] = check_stats_arg(args.vars)

        if args.stats is None:
            stats = None

    except MissingArgError as e:
        raise

    return (source_file, input_file, stats)