import argparse
import sys
from interpret_lib.errorhandler import MissingArgError


def args_parser():
    parser = argparse.ArgumentParser(description="Interpreter for IPPCode21")
    parser.add_argument("--source", nargs=1, help="XML file")
    parser.add_argument("--input", nargs=1, help="File for interpeter")

    args = parser.parse_args()

    source_file = sys.stdin
    input_file = sys.stdin

    try:
        if not args.source and not args.input:
            raise MissingArgError

        if args.source is not None:
            source_file = args.source[0]

        if args.input is not None:
            input_file = args.input[0]

    except MissingArgError as e:
        raise

    return (source_file, input_file)