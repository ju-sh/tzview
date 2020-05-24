"""
Test cases for code in src/tzview/__init__.py
"""

import argparse

import pytest

import tzview.app


@pytest.fixture
def parser():
    """
    Fixture returning an argparse.ArgumentParser
    """
    return tzview.app.create_parser()


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
                                  '--from-tz', 'Asia/Singapore',
                                  'Europe/Oslo', 'Asia/Istanbul'])
        assert args.dt == '2020-03-12 23:12:38'
        assert args.from_tz == 'Asia/Singapore'
        assert args.to_tzs == ['Europe/Oslo', 'Asia/Istanbul']


class TestMain:
    def test_valid(self):
        args = argparse.Namespace(dt='2020-03-12 12:34:56',
                                  from_tz='local',
                                  to_tzs=['Asia/Tokyo'])
        assert tzview.app.main(args) == 0

    def test_invalid(self):
        # Unknown time zone
        args = argparse.Namespace(dt='2020-03-12 12:34:56',
                                  from_tz='locl',
                                  to_tzs=['Asia/Tokyo'])
        assert tzview.app.main(args) == 1

        # Invalid datetime
        args = argparse.Namespace(dt='2020-03-12 82:34:56',
                                  from_tz='locl',
                                  to_tzs=['Asia/Tokyo'])
        assert tzview.app.main(args) == 1
