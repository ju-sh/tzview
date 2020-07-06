# tzview

<a href="https://pypi.org/project/tzview"><img alt="PyPI" src="https://img.shields.io/pypi/v/tzview"></a>
<img alt="Build Status" src="https://api.travis-ci.com/ju-sh/tzview.svg?branch=master"></img>
<a href="https://github.com/ju-sh/tzview/blob/master/LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/pypi/l/tzview"></a>

View datetime in different time zones.

Given a time zone and datetime, tzview can find the datetime at other time zones.

The time zone names are those as specified in the Olsen time zone database (tz).

tzview merely leverages `pytz` package to get the job done.

<h2>Installation</h2>

You need Python>=3.6 to use tzview.

It can be installed from PyPI with pip using

    pip install tzview

<h2>Usage</h2>

<h3>Defaults</h3>

The string `'local'` can be used to specify the local time zone. This is the source time zone by default.

The string `'now'` can be used to specify the local datetime. This is the source datetime by default.

In addition to the time zone names, tzview can also identify the time zone of a limited number of cities (Eg: Hanoi -> Asia/Ho\_Chi\_Minh).

<h3>Command line usage</h3>

To get the current time at Tokyo relative to your computer's current time and time zone, use

    python3 -m tzview Asia/Tokyo

to get something like

    09:47 PM, 06-Jul-2020 (+0900): Asia/Tokyo

You could provide source datetime using `--dt` option and source time zone with `--from-tz` option. Like

    python3 -m tzview --dt "2020-03-23 11:32:34" --from-tz Asia/Tokyo Europe/Oslo Africa/Bamako

to get an output like

    03:32 AM, 23-Mar-2020 (+0100): Europe/Oslo
    02:32 AM, 23-Mar-2020 (+0000): Africa/Bamako

The input and output datetime formats can be changed with options.

Use `python3 -m tzview --help` for more.

<h3>Usage as module</h3>

The `tzview()` function can be used. It accepts the extension name as string.

Return value would be a list of timezone aware datetimes.

For example,

    >>> from tzview import tzview
    >>> tzview(['Europe/Oslo'])  # Based on current time
    [datetime.datetime(2020, 5, 24, 12, 6, 14, 272335, tzinfo=<DstTzInfo 'Europe/Oslo' CEST+2:00:00 DST>)]


    >>> tzview(['Europe/Athens', 'Asia/Singapore'], dt_str="2020-May-24 13:11:07", dt_format="%Y-%b-%d %H:%M:%S")
    [datetime.datetime(2020, 5, 24, 10, 41, 7, tzinfo=<DstTzInfo 'Europe/Athens' EEST+3:00:00 DST>), datetime.datetime(2020, 5, 24, 15, 41, 7, tzinfo=<DstTzInfo 'Asia/Singapore' +08+8:00:00 STD>)]

<h2>Why</h2>

It is useful to figure out the time when you got to attend meetings coordinated from a different time zone.

Or when calling a friend at another timezone to know the time of the day there.

That's what I use it for. :-)

