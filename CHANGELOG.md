24-05-2020
----------
Version 0.2 released.

Modify `tzview.tzview()` function from

    def tzview(dt: datetime.datetime,
               from_tz: pytz.tzfile,
               to_tzs: List[pytz.tzfile]) -> List[datetime.datetime]:

to

    def tzview(to_tz_strs: List[str],
               from_tz_str: str = 'local',
               dt_str: str = 'now') -> List[datetime.datetime]:
