"""
Test cases for code in src/tzview/__init__.py
"""

import argparse

import pytest

import tzview.cli


@pytest.fixture
def parser():
    """
    Fixture returning an argparse.ArgumentParser
    """
    return tzview.cli.create_parser()


class TestCreateParser:
    def test_all_default(self, parser):
        """
        Test with all default values
        """
        args = parser.parse_args('Europe/Oslo'.split())
        assert args.dt == 'now'
        assert args.from_tz == 'local'
        assert args.to_tzs == ['Europe/Oslo']

    def test_all_non_default(self, parser):
        """
        Test with all non-default values
        """
        args = parser.parse_args(['--dt', '2020-03-12 23:12:38',
                                  '--in-format', '%Y-%m-%d %H:%M:%S',
                                  '--from-tz', 'Asia/Singapore',
                                  'Europe/Oslo', 'Asia/Istanbul'])
        assert args.dt == '2020-03-12 23:12:38'
        assert args.from_tz == 'Asia/Singapore'
        assert args.to_tzs == ['Europe/Oslo', 'Asia/Istanbul']


class TestMain:
    @pytest.mark.parametrize('args, expected_out', [
        # General
        (argparse.Namespace(dt='2020-03-12 12:34:56',
                            from_tz='Asia/Kolkata',
                            to_tzs=['Asia/Tokyo'],
                            in_format=None,
                            out_format="%I:%M %p, %d-%b-%Y (%z)"),
         "04:04 PM, 12-Mar-2020 (+0900): Asia/Tokyo\n"),

        # Use in_format option
        (argparse.Namespace(dt='03-2020-12 21:23:42',
                            from_tz='Europe/Istanbul',
                            to_tzs=['Asia/Tokyo'],
                            in_format='%d-%Y-%m %M:%H:%S',
                            out_format="%I:%M %p, %d-%b-%Y (%z)"),
         "05:21 AM, 04-Dec-2020 (+0900): Asia/Tokyo\n"),

        (argparse.Namespace(dt='03-2020-12 12:34:56',
                            from_tz='Europe/Istanbul',
                            to_tzs=['Asia/Tokyo', 'Europe/Oslo'],
                            in_format="%d-%Y-%m %H:%M:%S",
                            out_format='%H:%M'),
         "18:34: Asia/Tokyo\n10:34: Europe/Oslo\n"),
    ])
    def test_main(self, capsys, args, expected_out):
        assert tzview.cli.main(args) == 0
        captured = capsys.readouterr()
        assert captured.out == expected_out

    def test_now_dt(self):
        args = argparse.Namespace(dt='now',
                                  from_tz='Europe/Oslo',
                                  to_tzs=['Asia/Tokyo'],
                                  in_format=None,
                                  out_format="%I:%M %p, %d-%b-%Y (%z)")
        assert tzview.cli.main(args) == 0

    def test_local_tz(self):
        args = argparse.Namespace(dt='2020-03-12 12:34:56',
                                  from_tz='local',
                                  to_tzs=['Asia/Tokyo'],
                                  in_format=None,
                                  out_format="%I:%M %p, %d-%b-%Y (%z)")
        assert tzview.cli.main(args) == 0

    @pytest.mark.parametrize('args', [
        # Unknown time zone
        argparse.Namespace(dt='2020-03-12 12:34:56',
                           from_tz='locl',
                           to_tzs=['Asia/Dhaka'],
                           in_format=None,
                           out_format="%I:%M %p, %d-%b-%Y (%z)"),

        # Invalid datetime
        argparse.Namespace(dt='2020-03-12 82:34:56',
                           from_tz='local',
                           to_tzs=['Asia/Tokyo'],
                           in_format=None,
                           out_format="%I:%M %p, %d-%b-%Y (%z)")
    ])
    def test_invalid(self, args):
        assert tzview.cli.main(args) == 1
