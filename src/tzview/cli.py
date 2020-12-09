"""
Command line interface for tzview.
"""

import argparse
import tzcity
import tzview
from tzview.version import __version__


def create_parser() -> argparse.ArgumentParser:
    """
    Create a parser to parse the arguments provided to the CLI.

    Returns:
      The parser to parse CLI arguments.
    """
    parser = argparse.ArgumentParser(
        prog="tzview",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="View datetime in different time zones"
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + __version__
    )
    parser.add_argument('--dt', default='now')
    parser.add_argument('--from-tz', dest='from_tz', default='local')
    parser.add_argument('to_tzs', nargs='+')
    parser.add_argument('--in-format', dest='in_format')
    parser.add_argument('--out-format', dest='out_format',
                        default="%I:%M %p, %a, %d-%b-%Y (%z)")
    return parser


def main(args: argparse.Namespace) -> int:
    """
    The main function for the CLI.

    Returns:
      Non-zero on error and zero on successful operation.
    """
    try:
        # Call tzview
        to_dts = tzview.tzview(args.to_tzs, args.from_tz,
                               args.dt, args.in_format)
        for to_dt, to_tz in zip(to_dts, args.to_tzs):
            out_dt_str = to_dt.strftime(args.out_format)
            #out_to_tz = tzcity.capitalize(to_tz)
            #print(f"{out_dt_str}: {out_to_tz}")
            print(f"{out_dt_str}: {to_tz}")
    except ValueError as verr:
        print(verr)
        return 1

    return 0
