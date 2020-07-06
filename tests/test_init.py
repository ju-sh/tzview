"""
Test cases for code in src/tzview/__init__.py
"""

import datetime

import pytest
import pytz
import tzlocal

import tzview
import tzcity


class TestParseDT:
    @pytest.mark.parametrize('dt_str, dt_format, expected', [
        # Without dt_format
        ("2019-02-28 11:23:42", None,
         datetime.datetime(2019, 2, 28, 11, 23, 42)),
        ("May 2019 31", None,
         datetime.datetime(2019, 5, 31, 0, 0, 0)),

        # With dt_format
        ("31 19 05", "%d %y %m",
         datetime.datetime(2019, 5, 31, 0, 0, 0)),
    ])
    def test_valid(self, dt_str, dt_format, expected):
        """
        Normal valid test cases
        """
        assert tzview.parse_dt(dt_str, dt_format) == expected

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
        with pytest.raises(tzcity.UnknownTZCityException):
            tzview.parse_tz(tz_str)


class TestTZView:
    @pytest.mark.parametrize('to_tzs, from_tz, dt_str, dt_format, expected', [
       (['asia/dHaKa', 'America/Guayaquil'], 'Europe/Oslo',
        "2020-02-23 21:23:42", None, [(2, 23), (15, 23)]),

       # With dt_format
       (['asia/dHaKa', 'America/Guayaquil'], 'Europe/Oslo',
        "2020-February-23 21:23:42", "%Y-%B-%d %H:%M:%S",
        [(2, 23), (15, 23)]),

       # With city names (via tzcity package)
       (['caracas', 'bratislava'], 'oslo',
        "2020-February-23 21:23:42", None,
        [(16, 23), (21, 23)]),

        # Mixed. Both city and time zone names
       (['moscow', 'asia/Baku'], 'dushanbe',
        "31-Jan-2020", None,
        [(22, 0), (23, 0)]),
    ])
    def test_valid(self, to_tzs, from_tz, dt_str, dt_format, expected):
        """
        Valid usages
        """
        rv = tzview.tzview(to_tzs, from_tz, dt_str, dt_format)
        value = [(dt.hour, dt.minute) for dt in rv]
        assert value == expected

    @pytest.mark.parametrize('dt_str, to_tzs, from_tz, dt_format', [
        # Invalid hour
        ("2020-02-23 24:23:42", ['America/Guayaquil'], 'Europe/Oslo', None),

        # Unknown time zone name
        ("2020-02-23 21:23:42", ['America/Guayaquil'], 'Australia/Oslo', None),

        # Invalid dt_format
        ("-230-02-23 24:23:42", ['America/Guayaquil'], 'Europe/Oslo', "%d-%B"),
    ])
    def test_invalid(self, dt_str, to_tzs, from_tz, dt_format):
        """
        Test cases that should raise exception because of incorrect dt
        """
        with pytest.raises(ValueError):
            tzview.tzview(to_tzs, from_tz, dt_str)

    @pytest.mark.parametrize('dt_str, to_tzs, from_tz, dt_format', [
        # Invalid hour
        ("2020-02-23 22:23:42", ['Amrica/Guayaquil'], 'Europe/Oslo', None),
    ])
    def test_unknown_tzcity(self, dt_str, to_tzs, from_tz, dt_format):
        """
        Test cases that should raise exception because of unknown city
        of time zone name
        """
        with pytest.raises(ValueError) as ve:
            tzview.tzview(to_tzs, from_tz, dt_str)
