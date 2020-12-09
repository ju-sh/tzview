v0.4 ()
----
 * Allow pytz to recognzie tz name in `parse_tz()` before `tzcity()`

v0.3 (06-July-2020)
----
Version 0.3 released.

 * Use tzcity module for limited city name to time zone name mapping.

 * Add option `--in-format` to specify the format in which `--dt` is provided.
 * Add option `--out-format` to specify the format out of output datetimes.
 * `--dt` option can now have datetimes of arbitrary format (courtesy of dateutil.parser).
 * Parametrize some tests.


v0.2 (24-May-2020)
----
Version 0.2 released.

 * Modify `tzview.tzview()` function

Change signature from

    def tzview(dt: datetime.datetime,
               from_tz: pytz.tzfile,
               to_tzs: List[pytz.tzfile]) -> List[datetime.datetime]:

to

    def tzview(to_tz_strs: List[str],
               from_tz_str: str = 'local',
               dt_str: str = 'now') -> List[datetime.datetime]:
