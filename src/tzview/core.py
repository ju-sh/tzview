"""
Leave dt arithmetic to others

Incorporate to this command using
substitution (preferable) or xargs.

now means current time
local means current timezone
"""

from typing import List
import datetime

from tzcity.abbrs import TZ_ABBRS
import tzlocal
import pytz
import pytz.exceptions
import dateutil.parser
import tzcity


def _get_utcoffset(offset_str: str) -> int:
    """
    Return UTC offset in seconds
    """
    # Flag variable
    found = False

    if offset_str in TZ_ABBRS:
        hours = TZ_ABBRS[offset_str][0]
        minutes = TZ_ABBRS[offset_str][1]
        found = True

    #XXX: Combine all 3 regexs
    # For UTC+02
    mobj = re.match(r"^[+-]?\d\d$", offset_str)
    if mobj:
        hours = int(mobj.group(0))
        minutes = 0
        found = True

    # For UTC+02:30
    if not found:
        mobj = re.match(r"^([+-]?\d\d):(\d\d)$", offset_str)
        if mobj:
            hours = int(mobj.group(1))
            minutes = int(mobj.group(2))
            found = True

    # For UTC+0230
    if not found:
        mobj = re.match(r"^([+-]?\d\d)(\d\d)$", offset_str)
        if mobj:
            hours = int(mobj.group(1))
            minutes = int(mobj.group(2))
            found = True

    if not found:
        return ValueError("Unknown format")

    if (hours < -12) or (hours > 14) or (minutes > 59):
       raise ValueError(f"{offset_str}: invalid offset")
    return (hours * 3600) + (minutes * 60)


def parse_dt(dt_str: str, dt_format: str = None) -> datetime.datetime:
    """
    Convert datetime in string form to datetime object.

    dt_str: Input datetime as a string in %Y-%m-%d %H:%M:%S format.
    'now' indicates local time.

    Returns a naive datetime.datetime
    """
    dt_str = dt_str.strip().lower()
    if dt_str == 'now':
        dtime = datetime.datetime.now()
    elif dt_format is not None:  # if a format is provided, use it
        dtime = datetime.datetime.strptime(dt_str, dt_format)
    else:
        dtime = dateutil.parser.parse(dt_str)
    return dtime


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
    try:
        return pytz.timezone(tz_str)
    except pytz.exceptions.UnknownTimeZoneError:
        pass
    try:
        tz_name = tzcity.tzcity(tz_str)
        return pytz.timezone(tz_name)
    except pytz.exceptions.UnknownTimeZoneError as utze:
        raise ValueError("{tz_str}: ambiguous or unknown name") from utze


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
    dtime = parse_dt(dt_str, dt_format)
    from_dt = from_tz.localize(dtime)

    # Find target timezone datetimes
    to_dts = []
    for to_tz_str in to_tz_strs:
        to_tz = parse_tz(to_tz_str)
        to_dt = from_dt.astimezone(to_tz)
        to_dts.append(to_dt)

    return to_dts
