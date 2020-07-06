"""
Leave dt arithmetic to others

Incorporate to this command using
substitution (preferable) or xargs.

now means current time
local means current timezone
"""

from typing import List
import datetime

import tzlocal
import pytz
import pytz.exceptions
import dateutil.parser
import tzcity

# Stuff for mypy
# _pytz_tzinfo = Union[pytz.UTC.__class__,
#                     pytz.tzinfo.StaticTzInfo, pytz.tzinfo.DstTzInfo]
# _pytz_tzinfo = Union[pytz.tzinfo.StaticTzInfo, pytz.tzinfo.DstTzInfo]


def parse_dt(dt_str: str, dt_format: str = None) -> datetime.datetime:
    """
    Convert datetime in string form to datetime object.

    dt_str: Input datetime as a string in %Y-%m-%d %H:%M:%S format.
    'now' indicates local time.

    Returns datetime.datetime
    """
    dt_str = dt_str.strip().lower()
    if dt_str == 'now':
        dt = datetime.datetime.now()
    elif dt_format is not None:  # if a format is provided, use it
        dt = datetime.datetime.strptime(dt_str, dt_format)
    else:
        dt = dateutil.parser.parse(dt_str)
    return dt


def parse_tz(tz_str: str):
    """
    Converts time zone name to corresponding to pytz timezone.

    tz_str: Name of timezone
    'local' indicates local timezone

    Returns pytz timezone
    """
    tz_str = tz_str.strip().lower()
    if tz_str == 'local':
        return tzlocal.get_localzone()
    tz_name = tzcity.tzcity(tz_str)
    return pytz.timezone(tz_name)


def tzview(to_tz_strs: List[str],
           from_tz_str: str = 'local',
           dt_str: str = 'now',
           dt_format: str = None) -> List[datetime.datetime]:
    """
    to_tzs: list of tzs to which dt should be converted.
    from_tz: the time zone in which dt is in
    dt_str: datetime to be converted as a string.

    Accepts source time and timezone along with a list of timezones to
    which it should be converted to.

    Returns list of tz aware converted datetimes.
    """

    # Find source timezone
    from_tz = parse_tz(from_tz_str)

    # Find source datetime
    dt = parse_dt(dt_str, dt_format)
    from_dt = from_tz.localize(dt)

    # Find target timezone datetimes
    to_dts = []
    for to_tz_str in to_tz_strs:
        to_tz = parse_tz(to_tz_str)
        to_dt = from_dt.astimezone(to_tz)
        to_dts.append(to_dt)

    return to_dts
