"""
Test cases for code in src/tzview/__init__.py
"""

import datetime

import pytest
import pytz
import tzlocal

import tzview


class TestParseDT:
    @pytest.mark.parametrize('dt_str, expected', [
        ("2019-02-28 11:23:42",
         datetime.datetime(2019, 2, 28, 11, 23, 42)),
        ("May 2019 31",
         datetime.datetime(2019, 5, 31, 0, 0, 0)),
    ])
    def test_valid(self, dt_str, expected):
        """
        Normal valid test cases
        """
        assert tzview.parse_dt(dt_str) == expected

    def test_valid_now(self):
        """
        Valid test case when dt value is 'now'
        """
        now = datetime.datetime.now()
        rv = tzview.parse_dt("now")
        assert now-rv <= datetime.timedelta(seconds=2)

    @pytest.mark.parametrize('dt_str', [
        "23-30-34", "a3-3g-32", "two"
    ])
    def test_invalid(self, dt_str):
        """
        Test cases that should raise exception
        """
        with pytest.raises(ValueError):
            tzview.parse_dt(dt_str)


class TestParseTZ:
    @pytest.mark.parametrize('tz_str, expected', [
        ("local", tzlocal.get_localzone()),
        ("Europe/Oslo", pytz.timezone("Europe/Oslo")),
        ("Asia/Kuala_Lumpur", pytz.timezone("Asia/Kuala_Lumpur")),
    ])
    def test_valid(self, tz_str, expected):
        """
        Normal valid test cases
        """
        assert tzview.parse_tz(tz_str) == expected

    def test_valid_local(self):
        """
        Valid test case when tz_str value is 'local'
        """
        local = tzlocal.get_localzone()
        rv = tzview.parse_tz("local")
        assert local.zone == rv.zone

    @pytest.mark.parametrize('tz_str', [
        "now", "Europ/Oslo", "Asia/Kuala Lumpur"
    ])
    def test_invalid(self, tz_str):
        """
        Test cases that should raise exception
        """
        with pytest.raises(pytz.exceptions.UnknownTimeZoneError):
            tzview.parse_tz(tz_str)


class TestTZView:
    def test_tzview(self):
        """
        Valid test cases
        """
        dt_str = "2020-02-23 21:23:42"
        from_tz = 'Europe/Oslo'
        to_tzs = ['asia/dHaKa', 'America/Guayaquil']
        expected = [(2, 23), (15, 23)]
        rv = tzview.tzview(to_tzs, from_tz, dt_str)
        for to_dt, (hour, minute) in zip(rv, expected):
            assert to_dt.hour == hour
            assert to_dt.minute == minute

    def test_invalid_dt_str(self):
        """
        Test cases that should raise exception due to invalid datetime
        """
        dt_str = "2020-02-23 24:23:42"
        from_tz = 'Europe/Oslo'
        to_tzs = ['America/Guayaquil']
        with pytest.raises(ValueError):
            tzview.tzview(to_tzs, from_tz, dt_str)

    def test_invalid_tz_str(self):
        """
        Test cases that should raise exception due to invalid tz name
        """
        dt_str = "2020-02-23 21:23:42"
        from_tz = 'Europe/Olo'
        to_tzs = ['Ameria/Guayaquil']
        with pytest.raises(ValueError):
            tzview.tzview(to_tzs, from_tz, dt_str)
