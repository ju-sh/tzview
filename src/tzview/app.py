"""
Command line interface for tzview.
"""

__version__ = "0.3"
__author__ = "Julin S"

import argparse
import tzview
import tzcity


def create_parser() -> argparse.ArgumentParser:
    """
    Create the parser for the cli.

    Returns the parser object.
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
                        default="%I:%M %p, %d-%b-%Y (%z)")
    return parser


def main(args: argparse.Namespace) -> int:
    """
    The main function for the CLI.

    Returns non-zero on error and zero on successful operation.
    """
    no_exception = False
    try:
        # Call tzview
        to_dts = tzview.tzview(args.to_tzs, args.from_tz,
                               args.dt, args.in_format)
        for to_dt, to_tz in zip(to_dts, args.to_tzs):
            out_dt_str = to_dt.strftime(args.out_format)
            # if to_tz.lower() == 'local':
            #     out_to_tz = tzview.parse_tz('local').zone
            # else:
            #     out_to_tz = tzcity.capitalize(to_tz)
            out_to_tz = tzcity.capitalize(to_tz)
            print(f"{out_dt_str}: {out_to_tz}")
    except tzcity.UnknownTZCityException as utzce:
        print(f"Ambiguous or unknown name: {utzce.citytz}")
    except ValueError:
        print(f"Unable to parse datetime: {args.dt}")
    else:
        # This part runs only if no exception occurred in try block
        no_exception = True

    if no_exception:
        return 0
    return 1
