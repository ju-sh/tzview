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

<h3>Command line usage</h3>

To get the current time at Tokyo relative to your computer's current time and time zone, use

    python3 -m tzview Asia/Tokyo

to get something like

    2020-05-24 09:16:05.281238+09:00 : Asia/Tokyo

You could provide source datetime using `--dt` option and source time zone with `--from-tz` option. Like

    python3 -m tzview --dt "2020-03-23 11:32:34" --from-tz Asia/Tokyo Europe/Oslo Asia/Istanbul

to get an output like

    2020-03-23 03:32:34+01:00 : Europe/Oslo
    2020-03-23 05:32:34+03:00 : Asia/Istanbul

Use `python3 -m tzview --help` for more.

<h3>Usage as module</h3>

The `tzview()` function can be used. It accepts the extension name as string.

Return value would be a list of timezone aware datetimes.

For example,

    >>> from tzview import tzview
    >>> t(['Europe/Oslo'])
    [datetime.datetime(2020, 5, 24, 12, 6, 14, 272335, tzinfo=<DstTzInfo 'Europe/Oslo' CEST+2:00:00 DST>)]

    >>> t(['Europe/Athens', 'Asia/Singapore'])
    [datetime.datetime(2020, 5, 24, 13, 11, 7, 32042, tzinfo=<DstTzInfo 'Europe/Athens' EEST+3:00:00 DST>), datetime.datetime(2020, 5, 24, 18, 11, 7, 32042, tzinfo=<DstTzInfo 'Asia/Singapore' +08+8:00:00 STD>)]


<h2>Why</h2>

It is useful to figure meeting times when you got to attend meeting at a different time zone.

Or when calling a friend at another timezone to figure out the time of the day there.

That's what I use it for. :-)

