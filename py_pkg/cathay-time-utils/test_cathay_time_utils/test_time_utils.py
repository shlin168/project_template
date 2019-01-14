# -*- coding: utf-8 -*-

import pytest
from cathay_time_utils import TimeUtils


def test_cvt_timezone_utc2tw():
    base = '2018-09-10T00:00:00.000Z'
    utc_tz = 'UTC'
    tw_tz = 'Asia/Taipei'
    fmt = '%Y-%m-%dT%H:%M:%S.%fZ'

    result_dt = TimeUtils.cvt_timezone(
        base_tz=utc_tz, target_tz=tw_tz, base=base, fmt=fmt)
    result_str = result_dt.strftime("%Y-%m-%d %H:%M:%S")

    expected_result = '2018-09-10 08:00:00'
    assert result_str == expected_result


def test_cvt_timezone_tw_utc():
    base = '2018-09-10T08:00:00.000Z'
    utc_tz = 'UTC'
    tw_tz = 'Asia/Taipei'
    fmt = '%Y-%m-%dT%H:%M:%S.%fZ'

    result_dt = TimeUtils.cvt_timezone(
        base_tz=tw_tz, target_tz=utc_tz, base=base, fmt=fmt)
    result_str = result_dt.strftime("%Y-%m-%d %H:%M:%S")

    expected_result = '2018-09-10 00:00:00'
    assert result_str == expected_result


def test_validate_dtfmt():

    # expected success date
    TimeUtils.validate_dtfmt('2018-09-11', fmt='%Y-%m-%d')

    # expected error date
    with pytest.raises(ValueError):
        TimeUtils.validate_dtfmt('2018-09-11 15:00:00', fmt='%Y-%m-%d')

    # expected success fmt
    TimeUtils.validate_dtfmt('2018-09-11 15:00:00', fmt='%Y-%m-%d %H:%M:%S')

    # expected error fmt
    with pytest.raises(ValueError):
        TimeUtils.validate_dtfmt('2018-09-11 15:00:00', fmt='%Y-%m-%d')
