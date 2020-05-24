# tzview

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

    python3 -m tzview --dt "2020-03-23 11:32:34" --from-tz Asia/Tokyo Europe/Oslo Asia/Istanbul

would give

    2020-03-23 03:32:34+01:00 : Europe/Oslo
    2020-03-23 05:32:34+03:00 : Asia/Istanbul

<h3>Usage as module</h3>

The `tzview()` function can be used. It accepts the extension name as string.

Return value would be a list of lists.

Each sub-list corresponds to an entry related to that extension.

It consists of two elements:
 - The type of file which use the extension
 - The kind of software capable of manipulating such a file

For example,

    from tzview import tzview
    info = tzview("py")
    print(info)

would give

    [['Python script file', 'Python interpreter']]

and

    tzview("c")

returns

    [['C source file', 'C compilers'], ['Unix file archive', 'COMPACT']]

<h2>Why</h2>

It is useful to figure meeting times when you got to attend meeting at a different time zone.

Or when calling a friend at another timezone to figure out the time of the day there.

That's what I use it for. :-)

